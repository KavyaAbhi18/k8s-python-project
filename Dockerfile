FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

RUN mkdir -p /app/logs

EXPOSE 5000

CMD ["python", "app.py"]
