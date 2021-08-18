import json

from django.test import Client

from src.api.models import Issue
from integration.neo4j_test_case import Neo4jTestCase
from util.test_objects import TestObjects


class IssueViewTest(Neo4jTestCase):

    def setUp(self) -> None:
        self.new_issue = TestObjects.create_issue().save_new()
        self.assertIsNotNone(self.new_issue.id)

    def test_get_existing_issue_returns_issue(self):
        client = Client()

        resp = client.get(f'/api/nodes/{self.new_issue.id}')
        self.assertEquals(resp.status_code, 200)

        json_data = resp.json()['data']['data']

        self.assertEquals(self.new_issue.id, json_data['issueDetails']['id'])
        self.assertEquals(self.new_issue.issue_type, json_data['issueDetails']['issueType'])
        self.assertEquals(self.new_issue.related, json_data['issueDetails']['related'])

    def test_update_existing_issue_updates_issue_in_db(self):
        client = Client()

        new_description = "new description"
        issue_data = self.new_issue.get_node_repr()['data']['issueDetails']

        issue_data['issueDescription'] = new_description

        resp = client.post(f'/api/nodes/{self.new_issue.id}', data=json.dumps(issue_data), content_type="application/json")
        self.assertEquals(resp.status_code, 200)

        resp_issue_details = resp.json()['data']['data']['issueDetails']
        self.assertEquals(resp_issue_details['issueDescription'], new_description)

        self.assertEquals(Issue.get_by_id(self.new_issue.id).description, new_description)
