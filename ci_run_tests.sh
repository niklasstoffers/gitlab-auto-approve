#!/bin/sh
docker run --entrypoint /bin/sh -v "./tests:/tests" gitlab-auto-approve -c \
    "pip install -r /tests/requirements.txt && \
     pytest /tests"