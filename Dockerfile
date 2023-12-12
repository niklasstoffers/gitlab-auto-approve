FROM python:3.12
WORKDIR /app
COPY ./src /app
RUN pip install -r /app/requirements.txt
ENTRYPOINT ["python", "main.py"]