from enum import Enum

class MergeRequestStatus(str, Enum):
    BLOCKED = 'blocked_status'
    BROKEN_STATUS = 'broken_status'
    CHECKING = 'checking'
    UNCHECKED = 'unchecked'
    CI_MUST_PASS = 'ci_must_pass'
    CI_STILL_RUNNING = 'ci_still_running'
    DISCUSSIONS_NOT_RESOLVED = 'discussions_not_resolved'
    DRAFT_STATUS = 'draft_status'
    EXTERNAL_STATUS_CHECKS = 'external_status_checks'
    MERGEABLE = 'mergeable'
    NOT_APPROVED = 'not_approved'
    NOT_OPEN = 'not_open'
    POLICIES_DENIED = 'policies_denied'
    JIRA_ASSOCIATION_MISSING = 'jira_association_missing'