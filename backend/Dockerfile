FROM python:3.10.13-alpine3.18

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app/backend

# Install PostgreSQL client library and other build dependencies
RUN apk add --virtual .build-deps --no-cache postgresql-dev gcc python3-dev musl-dev \
    && apk add --no-cache libpq

COPY requirements.txt /app/backend/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Remove build dependencies and unused cache to reduce image size
RUN apk del .build-deps \
    && rm -rf /root/.cache

COPY . /app/backend/

CMD ["sh", "-c", "python manage.py wait_for_db --settings=config.settings.local && python manage.py runserver 0.0.0.0:8000 --settings=config.settings.local"]

