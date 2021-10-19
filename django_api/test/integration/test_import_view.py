from os import path

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client

from integration.neo4j_test_case import Neo4jTestCase


class ImportViewTest(Neo4jTestCase):
    def test_file_upload_should_create_issues(self):
        resource_path = f'{path.dirname(__file__)}/../util/upload_test.txt'

        with open(resource_path) as content:
            resp = Client().post('/api/nodes/import', {'issues': content})

        self.assertEqual(resp.status_code, 200)