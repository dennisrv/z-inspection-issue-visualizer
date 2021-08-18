from integration.neo4j_test_case import Neo4jTestCase
from src.api.models import Issue
from util.test_objects import TestObjects


class IssueTest(Neo4jTestCase):

    def test_create_issue(self):
        issue = TestObjects.create_issue()
        self.assertIsNone(issue.id)
        self.assertIsNone(issue.related_to, None)
        self.assertEquals(len(Issue.get_all()), 0)

        issue.save_new()

        self.assertIsNotNone(issue.id)
        self.assertEqual(len(issue.related_to), 2)
        self.assertEquals(len(Issue.get_all()), 1)

    def test_update_issue(self):
        issue = TestObjects.create_issue()
        issue.save_new()

        id_before = issue.id
        new_issue_title = "different title"
        issue.title = new_issue_title
        issue.related = [{
            "principle": "Fairness",
            "requirement": "Accountability",
            "subRequirement": "Auditability"
        }]
        issue.save_update()

        self.assertEquals(issue.id, id_before)
        # no new issue was created
        self.assertEquals(len(Issue.get_all()), 1)
        self.assertEquals(issue.title, new_issue_title)
        self.assertEquals(len(issue.related_to), 1)

        issue_from_db = Issue.get_by_id(id_before)
        self.assertEquals(issue, issue_from_db)
