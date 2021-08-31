from pathlib import Path

from django import setup as setup_django
from django.core.management import BaseCommand
from neomodel import (
    install_all_labels,
    clear_neo4j_database,
    db,
)


class Command(BaseCommand):
    """
    Based on django-neomodel install_labels command,
    https://github.com/neo4j-contrib/django-neomodel/blob/master/django_neomodel/management/commands/install_labels.py
    """
    help = "Install labels and constraints for neo4j database, populate database with Ethical Principles, " \
           "Key Requirements and Sub Requirements"

    def handle(self, *args, **options):
        setup_django()
        query_text = (Path(__file__).parents[0] / "populate_db.cql").read_text()
        clear_neo4j_database(db)
        install_all_labels(stdout=self.stdout)
        db.cypher_query(query_text)
