from autoapprove.helpers.type import is_optional


def test():
    assert is_optional(str | None)
