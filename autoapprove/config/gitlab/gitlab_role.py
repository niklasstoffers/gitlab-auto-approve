from enum import Enum
from services.gitlab.gitlab_role import GitlabRole as Role

ROLE_MAPPINGS = dict()


class GitlabRole(str, Enum):
    NO_ACCESS = 'NO_ACCESS'
    MINIMAL_ACCESS = 'MINIMAL_ACCESS'
    GUEST = 'GUEST'
    REPORTER = 'REPORTER'
    DEVELOPER = 'DEVELOPER'
    MAINTAINER = 'MAINTAINER'
    OWNER = 'OWNER'

    def get_role(self):
        return ROLE_MAPPINGS[self]


ROLE_MAPPINGS[GitlabRole.NO_ACCESS] = Role.NO_ACCESS
ROLE_MAPPINGS[GitlabRole.MINIMAL_ACCESS] = Role.MINIMAL_ACCESS
ROLE_MAPPINGS[GitlabRole.GUEST] = Role.GUEST
ROLE_MAPPINGS[GitlabRole.REPORTER] = Role.REPORTER
ROLE_MAPPINGS[GitlabRole.DEVELOPER] = Role.DEVELOPER
ROLE_MAPPINGS[GitlabRole.MAINTAINER] = Role.MAINTAINER
ROLE_MAPPINGS[GitlabRole.OWNER] = Role.OWNER
