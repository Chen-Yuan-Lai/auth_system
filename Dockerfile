FROM python:3.10.2-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/auth_system

COPY requirements.txt /usr/auth_system/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/auth_system/

CMD alembic upgrade head && uvicorn src.main:app --host 0.0.0.0 --port 8000