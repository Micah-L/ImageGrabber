# Dockerfile
FROM python:3.8
RUN apt-get update -y
RUN apt-get install -y --fix-missing python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools libglib2.0-0 libsm6 libxrender-dev libxext6
COPY . /app
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENV PORT 8080
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 wsgi:app
