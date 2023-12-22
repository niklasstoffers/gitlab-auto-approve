FROM python:3.12
WORKDIR /app
COPY ./src/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
ENTRYPOINT ["python", "main.py"]