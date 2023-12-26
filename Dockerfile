FROM python:3.12
WORKDIR /autoapprove
COPY ./autoapprove /autoapprove
COPY ./default_config.yaml /autoapprove/config.yaml
RUN pip install --no-cache-dir -r /autoapprove/requirements.txt
ENTRYPOINT ["python", "main.py"]