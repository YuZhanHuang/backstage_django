FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential netcat-openbsd \
  # psycopg dependencies
  && apt-get install -y libpq-dev \
  # Translations dependencies
  && apt-get install -y gettext \
  # Additional dependencies
  && apt-get install -y git procps curl \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*


RUN addgroup --system django \
    && adduser --system --ingroup django django


RUN pip install --upgrade pip wheel setuptools
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY ./compose/production/django/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//g' /entrypoint.sh
RUN chmod +x /entrypoint.sh
RUN chown django /entrypoint.sh

COPY ./compose/production/django/celery/entrypoint.sh /celery-entrypoint.sh
RUN sed -i 's/\r$//g' /celery-entrypoint.sh
RUN chmod +x /celery-entrypoint.sh
RUN chown django /celery-entrypoint.sh

COPY ./compose/production/django/start.sh /start.sh
RUN sed -i 's/\r$//g' /start.sh
RUN chmod +x /start.sh
RUN chown django /start.sh

COPY ./compose/production/django/celery/worker/start.sh /start-celeryworker.sh
RUN sed -i 's/\r$//g' /start-celeryworker.sh
RUN chmod +x /start-celeryworker.sh
RUN chown django /start-celeryworker.sh

COPY ./compose/production/django/celery/beat/start.sh /start-celerybeat.sh
RUN sed -i 's/\r$//g' /start-celerybeat.sh
RUN chmod +x /start-celerybeat.sh
RUN chown django /start-celerybeat.sh

COPY ./compose/production/django/celery/flower/start.sh /start-flower.sh
RUN sed -i 's/\r$//g' /start-flower.sh
RUN chmod +x /start-flower.sh
RUN chown django /start-flower.sh


RUN mkdir /app
RUN mkdir /app/staticfiles
RUN mkdir /app/mediafiles
WORKDIR /app

# copy project code
COPY . .

RUN chown -R django:django /app

USER django


ENTRYPOINT ["/entrypoint.sh"]