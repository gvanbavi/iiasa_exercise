FROM python:3.9
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP run.py
ENV DEBUG True

FROM ubuntu:latest
RUN apt-get update && apt-get install -y build-essential libproj-dev libgdal-dev gdal-bin python3-pip libpq-dev python3-dev

# install python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY env.sample .env

COPY . .


# gunicorn
CMD ["gunicorn", "--config", "gunicorn-cfg.py", "run:app"]
