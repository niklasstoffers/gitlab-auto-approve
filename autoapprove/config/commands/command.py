from abc import ABC
from pydantic import BaseModel, StringConstraints, validator
from typing import Annotated
from config.validators.string_list_not_empty import string_list_not_empty
from config.gitlab.gitlab_role import GitlabRole


class Command(ABC, BaseModel):
    keyword: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    ignore_case: bool
    strict_match: bool
    only_for_members: list[str] | None = None
    requires_role: GitlabRole | None = None

    _string_list_not_empty = validator('ONLY_FOR_MEMBERS', allow_reuse=True, check_fields=False)(string_list_not_empty)
