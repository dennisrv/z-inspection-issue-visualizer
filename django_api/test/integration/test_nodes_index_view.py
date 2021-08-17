import json
import os.path as path
from pathlib import Path

from django.test import (
    SimpleTestCase,
    Client,
)
from neomodel import (
    clear_neo4j_database,
    db,
    install_all_labels,
)


class NodeIndexTest(SimpleTestCase):

    @classmethod
    def setUpClass(cls) -> None:
        resource_path = f'{path.dirname(__file__)}/../resources/bootstrap_db.cql'
        query_text = Path(resource_path).read_text()
        clear_neo4j_database(db)
        install_all_labels()
        db.cypher_query(query_text)

    @classmethod
    def tearDownClass(cls):
        clear_neo4j_database(db, clear_constraints=True, clear_indexes=True)

    def tearDown(self) -> None:
        # delete all issues created during the test
        db.cypher_query("match (n:Issue) detach delete n")

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
