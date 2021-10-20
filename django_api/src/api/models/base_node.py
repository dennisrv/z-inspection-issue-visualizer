from __future__ import annotations

from typing import (
    Optional,
    List,
    Tuple,
    Dict
)

from neo4j.graph import Node
from neomodel import (
    RelationshipManager,
    StringProperty,
    StructuredNode, )
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


class BaseNode(BaseModel):
    # neo4j internal id, will not be used much
    id: Optional[int]
    title: str

    related_to: Optional[NodeList]

    class Config:
        orm_mode = True

    class OrmClass(StructuredNode):
        __abstract_node__ = True
        title = StringProperty(index=True)

        @classmethod
        def get_all(cls) -> List[BaseNode.OrmClass]:
            return cls.nodes.all()

        @classmethod
        def get_by_title(cls, *titles: str) -> List[BaseNode.OrmClass]:
            return cls.nodes.filter(title__in=titles)

        @classmethod
        def get_by_approximate_title(cls, *titles: str) -> List[BaseNode.OrmClass]:
            """
            Approximate title matching: use first word of provided title to check for
            nodes that start with the same title (case insensitive)
            :param titles:
            :return:
            """
            approximate_titles = [title.lower().split(" ")[0] for title in titles]
            found_nodes = [cls.nodes.first_or_none(title__istartswith=apx_title) for apx_title in approximate_titles]
            return [n for n in found_nodes if n is not None]

        @classmethod
        def get_by_id(cls, id_to_search: int) -> BaseNode.OrmClass:
            # hack to get the node by id, not sure if this should be changed later
            # as this is apparently not how it is supposed to be used
            node = cls(id=id_to_search)
            node.refresh()
            return node


    def to_cytoscape(self) -> Tuple[Dict[str, Dict], List[Dict[str, Dict]]]:
        return self.get_node_repr(), self.get_edges_repr()

    def get_node_repr(self) -> Dict[str, Dict]:
        return {
            'data': {
                'id': f'{self.id}',
                'label': self.title
            },
            'classes': self.cytoscape_class()
        }

    def get_edges_repr(self) -> List[Dict[str, Dict]]:
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

    def cytoscape_class(self) -> str:
        pass

    @classmethod
    def get_first(cls, **kwargs) -> Optional[BaseNode]:
        # get actual class of the generic type parameter
        data = cls.OrmClass.nodes.first_or_none(**kwargs)
        if data is None:
            return None
        return cls.from_orm(data)

    @classmethod
    def get_all(cls) -> List[BaseNode]:
        return [cls.from_orm(n) for n in cls.OrmClass.get_all()]

    @classmethod
    def get_by_title(cls, *titles: str) -> List[BaseNode]:
        return [cls.from_orm(n) for n in cls.OrmClass.get_by_title(*titles)]

    @classmethod
    def get_by_id(cls, id_to_search: int) -> BaseNode:
        return cls.from_orm(cls.OrmClass.get_by_id(id_to_search))

    @classmethod
    def from_raw(cls, raw_node: Node) -> BaseNode:
        return cls.from_orm(cls.OrmClass.inflate(raw_node))
