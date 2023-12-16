from gitlab import Gitlab
from config import config

def connect() -> Gitlab:
    gl = Gitlab(config.gitlab_host, private_token=config.access_token)
    try:
        gl.auth()
    except:
        raise Exception("Failed to connect to gitlab server. Please check your gitlab configuration.")
    return gl

gl: Gitlab = connect()