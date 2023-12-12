import gitlab
from config import config

def connect() -> gitlab.Gitlab:
    gl = gitlab.Gitlab(config.gitlab_host, private_token=config.access_token)
    try:
        gl.auth()
    except:
        raise Exception("Failed to connect to gitlab server")
    return gl

gl: gitlab.Gitlab = connect()