FROM python:3.12
WORKDIR /autoapprove
COPY ./autoapprove/requirements.txt /app/requirements.txt
COPY ./default_config.yaml /config/config.yaml
COPY ./tests/requirements.txt /tests/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
RUN pip install --no-cache-dir -r /tests/requirements.txt
ENTRYPOINT ["python", "main.py", "--startup-log-level", "DEBUG", "-c", "/config/config.yaml"]