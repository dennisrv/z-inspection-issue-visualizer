import os
from os import path
from pathlib import Path

from django.test import SimpleTestCase, override_settings
from neomodel import (
    clear_neo4j_database,
    db,
    install_all_labels,
)

from util import test_settings


class Neo4jTestCase(SimpleTestCase):

    @classmethod
    def setUpClass(cls) -> None:
        db.set_connection(test_settings.NEO4J_BOLT_URL)
        resource_path = f'{path.dirname(__file__)}/../util/bootstrap_db.cql'
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
