FROM python:3.13-slim

WORKDIR /upwards.crm.backend/

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONNUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    musl-dev \
    postgresql-server-dev-all \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /upwards.crm.backend/
RUN pip install --upgrade pip && pip install -r requirements.txt
    
COPY . /upwards.crm.backend/

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
# CMD ["python", "app/manage.py", "runserver", "0.0.0.0:8000"]