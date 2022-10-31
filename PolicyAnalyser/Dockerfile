FROM python:3



ENV PYTHONDONTWRITEBYTECODE=1   

ENV  PYTHONUNBUFFERED 1

WORKDIR /app

ADD . /app

COPY ./requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install -r requirements.txt

COPY . /app