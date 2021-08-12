from neomodel import config

config.DATABASE_URL = "bolt://neo4j:test@localhost:7687"
from .ethical_principle import EthicalPrinciple
from .key_requirement import KeyRequirement
from .sub_requirement import SubRequirement