FROM python:3.12
WORKDIR /app
COPY ./src/requirements.txt /app/requirements.txt
COPY ./default_config.yaml /config/config.yaml
RUN pip install --no-cache-dir -r /app/requirements.txt
ENTRYPOINT ["python", "main.py", "--startup-log-level", "DEBUG", "-c", "/config/config.yaml"]