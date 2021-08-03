from neomodel import config

config.DATABASE_URL = "bolt://neo4j:test@localhost:7687"
from .ethical_principle import EthicalPrinciple