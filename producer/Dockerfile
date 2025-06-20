FROM python:3.12.11-slim

RUN apt-get update && apt-get install -y && apt-get clean

WORKDIR /producer

# COPY requirements.txt .
# COPY producer.py .
COPY . .
ENV PYTHONPATH=/producer

RUN pip install --upgrade pip && pip install -r requirements.txt

# Run the application
CMD ["python", "-u", "producer.py"]