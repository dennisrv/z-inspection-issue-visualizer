from __future__ import annotations

from typing import (
    TypeVar,
    Generic,
    Optional,
    get_args,
    List,
    Tuple,
    Dict
)

from neomodel import (
    RelationshipManager,
    StringProperty,
    StructuredNode,
    UniqueIdProperty,
)
from pydantic import BaseModel


class NodeList(object):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        # __modify_schema__ should mutate the dict it receives in place,
        # the returned value will be ignored
        field_schema.update(
            # simplified regex here for brevity, see the wikipedia link above
            description='List of integers representing the ids of nodes this '
                        'node is connected to via the relationship RELATED_TO',
            # some example postcodes
            examples=['1234', '100028'],
        )

    @classmethod
    def validate(cls, instance: RelationshipManager) -> List[int]:
        if not isinstance(instance, RelationshipManager):
            raise TypeError('RelationshipManager required')

        return [node.id for node in instance.all()]

    def __repr__(self):
        return f'NodeRelationship({[node.id for node in self.all()]})'


class BaseNodeOrm(StructuredNode):
    __abstract_node__ = True
    id = UniqueIdProperty()
    title = StringProperty()


OrmClass = TypeVar('OrmClass', bound=BaseNodeOrm)


def get_generic_class(cls):
    return get_args(cls.__orig_bases__[0])[0]


class BaseNode(BaseModel, Generic[OrmClass]):
    id: int
    title: str

    related_to: Optional[NodeList]

    class Config:
        orm_mode = True

    def to_cytoscape(self) -> Tuple[Dict[str, object], List[Dict[str, object]]]:
        return self.get_node_repr(), self.get_edges_repr()

    def get_node_repr(self) -> Dict[str, object]:
        return {
            'data': {
                'id': f'{self.id}',
                'label': self.title
            },
            'classes': self.cytoscape_class()
        }

    def get_edges_repr(self) -> List[Dict[str, object]]:
        if self.related_to is None:
            return []
        else:
            return [{
                'data': {
                    'id': f'{self.id}-{target_node_id}',
                    'source': f'{self.id}',
                    'target': f'{target_node_id}'
                }
            } for target_node_id in self.related_to]

    def cytoscape_class(self):
        pass

    @classmethod
    def get_first(cls, **kwargs) -> Optional[BaseNode]:
        # get actual class of the generic type parameter
        data = get_generic_class(cls).nodes.first_or_none(**kwargs)
        if data is None:
            return None
        return cls.from_orm(data)

    @classmethod
    def get_all(cls) -> Optional[List[BaseNode]]:
        data = get_generic_class(cls).nodes.all()
        if data is None:
            return None
        return [cls.from_orm(d) for d in data]
