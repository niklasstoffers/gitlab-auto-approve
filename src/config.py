from pydantic import BaseModel, ValidationError
import yaml

class Approval(BaseModel):
    keyword: str
    ignore_case: bool
    strict_match: bool
    only_for_members: list[str] | None
    message: str | None

class Config(BaseModel):
    gitlab_host: str
    access_token: str
    webhook_token: str
    approval: Approval

def load_config(filename: str = "config.yaml") -> Config:
    try:
        with open(filename) as config_file:
            yaml_config = yaml.safe_load(config_file.read())
            config: Config = Config(**yaml_config)
            return config
    except ValidationError:
        raise Exception("Failed to load configuration file. Please check your settings")
    
config: Config = load_config()