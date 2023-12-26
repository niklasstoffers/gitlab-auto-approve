from enum import Enum


class GitlabRole(Enum):
    NO_ACCESS = 0
    MINIMAL_ACCESS = 5
    GUEST = 10
    REPORTER = 20
    DEVELOPER = 30
    MAINTAINER = 40
    OWNER = 50

    def is_higher_than(self, role: 'GitlabRole') -> bool:
        return self > role
