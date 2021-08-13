from django.apps import AppConfig
from neomodel import (
    config,
    install_all_labels
)

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.api'
    verbose_name = "Neo4j REST API"

    def ready(self):
        config.DATABASE_URL = "bolt://neo4j:test@localhost:7687"
        install_all_labels()
