FROM python:3.10-alpine as python
ENV PYTHONUNBUFFERED=true
WORKDIR /app

FROM python as intermediate
ENV PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_NO_INTERACTION=1 \
    POETRY_HOME=/opt/poetry \
    POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN apk add --no-cache build-base wget curl ca-certificates openssl tar openssh postgresql-dev libffi-dev zlib-dev jpeg-dev

RUN curl -sSL https://install.python-poetry.org | python -
COPY poetry.lock pyproject.toml ./
RUN poetry install --without test,dev --no-root -v

FROM python
RUN apk add --update --no-cache bash ca-certificates openssl postgresql-dev libffi-dev zlib-dev jpeg-dev
ENV PYTHONPATH="${PYTHONPATH}:/app" \
    DJANGO_SETTINGS_MODULE="ybls.settings.prod"
ENV PATH="/app/.venv/bin:$PATH"
COPY --from=intermediate /app/.venv/ /app/.venv
COPY ybls /app/ybls
RUN django-admin collectstatic --noinput --settings ybls.settings.base
EXPOSE 8000
CMD [ "bash", "-c", \
      "django-admin migrate && gunicorn -b 0.0.0.0:8000 --workers 2 --access-logfile=- --timeout 120 ybls.wsgi:application" ]