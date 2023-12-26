from enum import Enum

class CommentEventType(str, Enum):
    NONE: str = "none"
    COMMIT: str = "commit"
    MERGE_REQUEST: str = "merge_request"
    ISSUE: str = "issue"
    SNIPPET: str = "snippet"