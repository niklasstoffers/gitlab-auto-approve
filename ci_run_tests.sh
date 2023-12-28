#!/bin/sh
mkdir coverage_report
docker run --entrypoint /bin/sh -v "./tests:/tests" -v "./coverage_report:/coverage_report" --mount type=bind,source=./.coveragerc,target=/.coveragerc gitlab-auto-approve -c \
    "cd / && \
     pip install -r tests/requirements.txt && \
     coverage run && \
     coverage xml && \
     mv coverage.xml coverage_report"