from pydantic import BaseModel, ValidationError
import yaml
from os import environ

class Approval(BaseModel):
    keyword: str
    ignore_case: bool
    strict_match: bool
    only_for_members: list[str] | None
    message: str | None

class SSL(BaseModel):
    enable: bool
    key_file: str
    cert_file: str

class Uvicorn(BaseModel):
    reload: bool

class Config(BaseModel):
    gitlab_host: str
    access_token: str
    webhook_token: str
    trusted_hosts_only: bool
    ssl: SSL
    approval: Approval
    uvicorn: Uvicorn

def get_bool_env(env_name: str, default_value: bool) -> bool:
    return environ.get(env_name, str(default_value)).lower() == 'true'

def get_list_env(env_name: str, default_value: list[str] | None) -> list[str] | None:
    env_value: str | None = environ.get(env_name)
    if env_value is None or len(env_value.strip()) == 0:
        return default_value
    return [s.strip() for s in env_value.strip().split(',')]

def load_env(config: Config):
    config.gitlab_host = environ.get('GITLAB_HOST', config.gitlab_host)
    config.access_token = environ.get('GITLAB_ACCESS_TOKEN', config.access_token)
    config.webhook_token = environ.get('GITLAB_WEBHOOK_TOKEN', config.webhook_token)
    config.trusted_hosts_only = get_bool_env('TRUSTED_HOSTS_ONLY', config.trusted_hosts_only)
    config.ssl.enable = get_bool_env('USE_SSL', config.ssl.enable)
    config.ssl.key_file = environ.get('SSL_KEYFILE', config.ssl.key_file)
    config.ssl.cert_file = environ.get('SSL_CERTFILE', config.ssl.cert_file)
    config.approval.keyword = environ.get('APPROVAL_KEYWORD', config.approval.keyword)
    config.approval.ignore_case = get_bool_env('APPROVAL_IGNORE_CASE', config.approval.ignore_case)
    config.approval.strict_match = environ.get('APPROVAL_STRICT_MATCH', config.approval.strict_match)
    config.approval.only_for_members = get_list_env('APPROVAL_ONLY_FOR_MEMBERS', config.approval.only_for_members)
    config.approval.message = environ.get('APPROVAL_MESSAGE', config.approval.message)
    config.uvicorn.reload = get_bool_env('UVICORN_RELOAD', config.uvicorn.reload)
    
    if config.approval.message is not None and len(config.approval.message.strip()) == 0:
        config.approval.message = None


def load_config(filename: str = "config.yaml") -> Config:
    try:
        with open(filename) as config_file:
            yaml_config = yaml.safe_load(config_file.read())
            config: Config = Config(**yaml_config)
            load_env(config)
            return config
    except ValidationError:
        raise Exception("Failed to load configuration file. Please check your settings")
    
config: Config = load_config()