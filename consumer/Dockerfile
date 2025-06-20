FROM python:3.12.11-slim

RUN apt-get update && apt-get install -y && apt-get clean

WORKDIR /consumer

# COPY requirements.txt .
# COPY consumer.py .
COPY . .
ENV PYTHONPATH=/consumer

RUN pip install --upgrade pip && pip install -r requirements.txt

# Run the application
# python -u allows for unbuffered output -> print statements are shown in real time in the terminal
CMD ["python", "-u", "consumer.py"]