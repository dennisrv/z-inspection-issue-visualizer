import json
import random
import string

from django.test import (
    Client,
)

from integration.neo4j_test_case import Neo4jTestCase
from util.test_objects import TestObjects


class IndexViewTest(Neo4jTestCase):

    def test_get_index_should_return_200_and_data(self):
        client = Client()
        resp = client.get('/api/nodes/')
        self.assertEqual(200, resp.status_code)

        json_data = resp.json()
        self.assertEqual(len(json_data.keys()), 2)

        self.assertEqual(json_data['status'], "success")
        self.assertGreater(len(json_data['data']['nodes']), 0)
        self.assertGreater(len(json_data['data']['edges']), 0)

    def test_post_nodes_should_create_new_issue(self):
        client = Client()
        form_data = {
            "issueType": "ethical-issue",
            "areas": [
                "Ethical",
                "Medical"
            ],
            "related": [
                {
                    "principle": "Respect for human autonomy",
                    "requirement": "Human agency and oversight",
                    "subRequirement": "Fundamental rights"
                },
                {
                    "principle": "Fairness",
                    "requirement": "Accountability",
                    "subRequirement": "Auditability"
                }
            ],
            "issueTitle": "Issue title",
            "issueDescription": "Some long text belongs down here.\nThis is just a placeholder."
        }
        resp = client.post('/api/nodes/', data=json.dumps(form_data), content_type="application/json")
        self.assertEqual(resp.status_code, 200)

        json_data = resp.json()
        self.assertEqual(json_data['status'], "success")
        self.assertIsNotNone(json_data['data'].get('node'))
        self.assertIsNotNone(json_data['data']['node'].get('data'))
        self.assertEqual(len(json_data['data']['edges']), 2)

    def test_post_with_missing_arguments_should_return_which_missing(self):
        client = Client()
        form_data_with_missing = {
            "areas": [
                "Ethical",
                "Medical"
            ],
            "related": [
                {
                    "principle": "Respect for human autonomy",
                    "requirement": "Human agency and oversight",
                    "subRequirement": "Fundamental rights"
                },
                {
                    "principle": "Fairness",
                    "requirement": "Accountability",
                    "subRequirement": "Auditability"
                }
            ],
            "issueDescription": "Some long text belongs down here.\nThis is just a placeholder."
        }
        resp = client.post('/api/nodes/', data=json.dumps(form_data_with_missing), content_type="application/json")
        self.assertEqual(resp.status_code, 400)

        json_data = resp.json()

        self.assertEqual(json_data['status'], "fail")
        self.assertIsNotNone(json_data['data'])
        self.assertGreater(len(json_data['data']), 0)
        # ensure the error description contains information on the missing parameters
        self.assertIsNotNone(json_data['data']['issueTitle'])
        self.assertIsNotNone(json_data['data']['issueType'])

    def test_get_filter_should_search_in_title_and_description(self):
        rnd = random.Random()
        random_string = ''.join(rnd.choices(string.ascii_uppercase + string.digits, k=10))
        text_to_search = f"I am looking for this text with a random number at the end {random_string}"

        non_matching_issues = [TestObjects.create_issue() for _ in range(5)]
        for i in non_matching_issues:
            i.save_new()

        matching_title_issue = TestObjects.create_issue()
        matching_title_issue.title += text_to_search
        matching_title_issue.save_new()

        matching_description_issue = TestObjects.create_issue()
        matching_description_issue.description += text_to_search + matching_title_issue.description
        matching_description_issue.save_new()

        client = Client()
        resp = client.get('/api/nodes/', {'searchText': text_to_search}, HTTP_ACCEPT='application/json')

        self.assertEqual(resp.status_code, 200)

        json_data = resp.json()
        self.assertEqual(json_data['status'], 'success')
        self.assertIsNotNone(json_data['data'])

        nodes = json_data['data']['nodes']
        edges = json_data['data']['edges']

        returned_issue_nodes = [n for n in nodes if "issue" in n['classes']]
        self.assertEqual(len(returned_issue_nodes), 2)
        self.assertGreaterEqual(len(nodes),
                                5)  # 2 issues + >=1 sub_requirement + >=1 key_requirement + >=1 ethical principle
        self.assertGreater(len(edges), 4)

    def test_filter_should_accept_one_related(self):
        test_issues = [TestObjects.create_issue() for _ in range(5)]
        for i in test_issues:
            i.save_new()

        principle = test_issues[0].related[0]['principle']
        resp = Client().get('/api/nodes/', {'related[]': principle}, HTTP_ACCEPT='application_json')
        self.assertEqual(resp.status_code, 200)

        json_data = resp.json()
        self.assertEqual(json_data['status'], 'success')
        self.assertIsNotNone(json_data['data'])

        nodes = json_data['data']['nodes']
        edges = json_data['data']['edges']

        returned_issues = [n for n in nodes if "issue" in n['classes']]
        self.assertGreaterEqual(len(returned_issues), 1)
        self.assertGreaterEqual(len(edges), 3)

    def test_filter_should_accept_multiple_related(self):
        test_issues = [TestObjects.create_issue() for _ in range(5)]
        for i in test_issues:
            i.save_new()

        principle = test_issues[0].related[0]['principle']
        key_requirement = test_issues[1].related[0]['requirement']
        sub_requirement = test_issues[2].related[0]['subRequirement']

        resp = Client().get('/api/nodes/', {'related[]': (principle, key_requirement, sub_requirement)},
                            HTTP_ACCEPT='application_json')

        self.assertEqual(resp.status_code, 200)

        json_data = resp.json()
        self.assertEqual(json_data['status'], 'success')
        self.assertIsNotNone(json_data['data'])

        nodes = json_data['data']['nodes']
        edges = json_data['data']['edges']

        returned_issues = [n for n in nodes if "issue" in n['classes']]
        self.assertGreaterEqual(len(returned_issues), 3)
        self.assertGreaterEqual(len(edges), 5)
