from django.apps import AppConfig
from django.conf import settings
from neomodel import config

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.api'
    verbose_name = "Neo4j REST API"

    def ready(self):
        config.DATABASE_URL = getattr(settings, "NEO4J_BOLT_URL")
        # install_all_labels()
