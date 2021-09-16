from __future__ import annotations

from enum import Enum
from typing import (
    List,
    Dict, Union, Set,
)

from neomodel import (
    RelationshipTo,
    OneOrMore,
    ArrayProperty,
    StringProperty,
    BooleanProperty,
)
from pydantic import Field

from src.utils import flatten
from .base_node import BaseNode
from .sub_requirement import SubRequirement


class IssueTypeEnum(str, Enum):
    ethical_issue = "ethical-issue"
    flag = "flag"


class RelatedWrapper(list):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        # __modify_schema__ should mutate the dict it receives in place,
        # the returned value will be ignored
        field_schema.update(
            description='Wrapper because neo4j does not allow nested lists and the position '
                        'of elements has meaning: 1st: principle, 2nd: requirement, 3rd: subRequirement '
                        'and this allows us to parse that list into dicts with the correct naming',
            # some example postcodes
            examples=['1234', '100028'],
        )

    @classmethod
    def validate(cls, instance: Union[List[str], List[Dict[str, str]]]) -> List[Dict[str, str]]:
        # somewhat hacky solution to handle neo4j data where all related are stored in one long
        # list and frontend data, where related can be nicely stored in dicts
        if len(instance) > 0:
            if isinstance(instance[0], dict):
                return instance
            elif len(instance) % 3 != 0:
                raise TypeError('Number of related elements must be a multiple of 3')
        return [{
            "principle": instance[i],
            "requirement": instance[i + 1],
            "subRequirement": instance[i + 2]
        } for i in range(0, len(instance), 3)]


class Issue(BaseNode):
    areas: List[str]
    # define field aliases for easier conversion between js field names and python field names
    description: str = Field(alias="issueDescription")
    issue_type: IssueTypeEnum = Field(alias="issueType")
    related: RelatedWrapper
    title: str = Field(alias="issueTitle")
    is_deleted: bool = False

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

    class OrmClass(BaseNode.OrmClass):
        # use __label__ if node label should not be the same as the class name
        # taken from https://stackoverflow.com/a/43458696
        __label__ = "Issue"

        areas = ArrayProperty(base_property=StringProperty())
        description = StringProperty()
        issue_type = StringProperty(choices={
            "ethical-issue": "Ethical Issue",
            "flag": "Flag"
        })
        related = ArrayProperty(base_property=StringProperty())
        is_deleted = BooleanProperty()

        related_to = RelationshipTo(SubRequirement.OrmClass, 'RELATED_TO', cardinality=OneOrMore)

        @classmethod
        def get_all(cls) -> List[Issue.OrmClass]:
            return cls.nodes.filter(is_deleted=False)

    def get_node_repr(self) -> Dict[str, Dict]:
        node_repr = super().get_node_repr()
        node_repr['data'].update(issueDetails={
            'id': self.id,
            'issueType': self.issue_type,
            'areas': self.areas,
            'related': self.related,
            'issueTitle': self.title,
            'issueDescription': self.description
        })
        return node_repr

    def cytoscape_class(self) -> str:
        return "issue"

    def save_new(self):
        # don't use current issue id (will be set by db)
        return self._save(params_to_exclude={'id', 'related_to'})

    def save_update(self):
        # issue exists in db => issue has id => id can be used
        return self._save(params_to_exclude={'related_to'})

    def _save(self, params_to_exclude: Set[str]) -> Issue:
        issue_dict = self.dict(exclude=params_to_exclude)
        issue_dict['related'] = flatten([rel.values() for rel in self.related])
        issue_dict['issue_type'] = issue_dict['issue_type'].value
        orm_issue = self.OrmClass(**issue_dict).save()

        self.id = orm_issue.id
        self.related_to = []

        orm_issue.related_to.disconnect_all()
        if len(self.related) > 0:
            related_sub_requirements = [rel['subRequirement'] for rel in self.related]
            for rel_req in SubRequirement.OrmClass.get_by_title(*related_sub_requirements):
                orm_issue.related_to.connect(rel_req)
                self.related_to.append(rel_req.id)

        return self
