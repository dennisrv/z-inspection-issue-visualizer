from unittest import TestCase

from django_api.src.api.models.base_node import (
    BaseNode,
)


class TestBaseNode(TestCase):
    node_id = 123
    node_title = 'some title'

    def test_create_from_dict(self):
        parameters = {
            'title': self.node_title
        }
        base_node = BaseNode(**parameters)
        self.assertEqual(self.node_title, base_node.title)
        self.assertIsNone(base_node.id)
        self.assertIsNone(base_node.related_to)

