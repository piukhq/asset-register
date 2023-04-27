FROM ghcr.io/binkhq/python:3.11-pipenv
ARG COMMIT="GITHASH"

WORKDIR /app
COPY Pipfile Pipfile.lock /app/

RUN pipenv install --system --deploy --ignore-pipfile

COPY asset_register /app/asset_register/
COPY entrypoint.sh /entrypoint

WORKDIR /app/asset_register
RUN sed -i "s@__VERSION__@$(date +%Y-%m-%dT%H:%M:%S-)${COMMIT}@g" asset_register/settings.py

ENTRYPOINT ["/entrypoint"]
CMD ["gunicorn", "-c", "gunicorn.py", "asset_register.wsgi"]
