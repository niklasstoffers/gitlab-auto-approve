from enum import Enum

class Environment(str, Enum):
    DEVELOPMENT = 'DEVELOPMENT'
    PRODUCTION = 'PRODUCTION'