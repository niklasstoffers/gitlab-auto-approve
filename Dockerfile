FROM python:3.12
WORKDIR /app
COPY ./src /app
COPY config.yaml /app/
RUN pip install -r /app/requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]