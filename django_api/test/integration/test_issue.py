from integration.neo4j_test_case import Neo4jTestCase
from src.api.models import Issue
from src.api.models.utils import filter_issues
from util.test_objects import TestObjects


class IssueTest(Neo4jTestCase):

    def test_create_issue(self):
        issue = TestObjects.create_issue()
        self.assertIsNone(issue.id)
        self.assertIsNone(issue.related_to)
        self.assertEquals(len(Issue.get_all()), 0)

        issue.save_new()

        self.assertIsNotNone(issue.id)
        self.assertIsNotNone(issue.related_to)
        self.assertGreaterEqual(len(issue.related_to), 1)
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

    def test_filter_issue(self):
        related_issues = [TestObjects.create_issue() for _ in range(5)]
        for issue in related_issues:
            # ensure issues relate to this
            issue.related = list({v['subRequirement']: v for v in issue.related + [{
                "principle": "Fairness",
                "requirement": "Accountability",
                "subRequirement": "Auditability"
            }]}.values())
            issue.save_new()

        unrelated_issues = [TestObjects.create_issue() for _ in range(5)]
        for issue in unrelated_issues:
            # ensure issues don't relate to this
            issue.related = [rel for rel in issue.related if rel['subRequirement'] != "Auditability"]
            issue.save_new()

        fairness_nodes = filter_issues(titles_of_related_nodes=['Fairness'])

        fairness_issues = [i for i in fairness_nodes if type(i) is Issue]
        self.assertEqual(len(fairness_issues), 5)

        self.assertEqual(len(fairness_nodes), 8)  # 5 issues + requirements + principle
