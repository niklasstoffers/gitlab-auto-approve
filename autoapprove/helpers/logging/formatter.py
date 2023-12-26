from uvicorn.logging import DefaultFormatter
default_formatter = DefaultFormatter(fmt="%(levelprefix)s [%(name)s] %(asctime)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
