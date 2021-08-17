from __future__ import annotations

from enum import Enum
from typing import (
    List,
    Dict,
)

from neomodel import (
    RelationshipTo,
    OneOrMore,
    ArrayProperty,
    StringProperty,
)
from pydantic import Field

from utils import flatten
from .base_node import (
    BaseNode,
    BaseNodeOrm,
)
from .sub_requirement import SubRequirementOrm, SubRequirement


class IssueOrm(BaseNodeOrm):
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

    related_to = RelationshipTo(SubRequirementOrm, 'RELATED_TO', cardinality=OneOrMore)


class IssueTypeEnum(str, Enum):
    ethical_issue = "ethical-issue"
    flag = "flag"


class Issue(BaseNode[IssueOrm]):
    areas: List[str]
    # define field aliases for easier conversion between js field names and python field names
    description: str = Field(alias="issueDescription")
    issue_type: IssueTypeEnum = Field(alias="issueType")
    related: List[Dict[str, str]]
    title: str = Field(alias="issueTitle")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

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

    def save(self) -> Issue:
        # omit values set via db later
        issue_dict = self.dict(exclude={'related_to', 'id'})
        issue_dict['related'] = flatten([rel.values() for rel in self.related])
        issue_dict['issue_type'] = issue_dict['issue_type'].value
        orm_issue = IssueOrm(**issue_dict).save()

        self.id = orm_issue.id
        self.related_to = []

        related_sub_requirements = [rel['subRequirement'] for rel in self.related]
        for rel_req in SubRequirement.get_by_title(*related_sub_requirements):
            orm_issue.related_to.connect(rel_req)
            self.related_to.append(rel_req.id)

        return self
