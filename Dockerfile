FROM python:3.12
WORKDIR /app
COPY ./src /app
COPY ./base_config.yaml /app/config.yaml
RUN pip install --no-cache-dir -r /app/requirements.txt
ENTRYPOINT ["python", "main.py"]