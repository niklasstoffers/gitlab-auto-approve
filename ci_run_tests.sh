#!/bin/sh
mkdir coverage_report
docker run --entrypoint /bin/sh -v "./tests:/tests" -v "./coverage_report:/coverage_report" gitlab-auto-approve -c \
    "pip install -r /tests/requirements.txt && \
     coverage run &&
     mv .coverage coverage_report"