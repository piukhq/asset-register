FROM binkhq/python:3.8
ARG COMMIT="GITHASH"

WORKDIR /app
COPY poetry.lock pyproject.toml /app/

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    pip install --no-cache-dir poetry psycopg2-binary && \
    poetry config virtualenvs.create false --local && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists

RUN poetry install --no-dev --no-root

COPY asset_register /app/asset_register/
COPY entrypoint.sh /entrypoint

WORKDIR /app/asset_register
RUN sed -i "s@__VERSION__@$(date +%Y-%m-%dT%H:%M:%S-)${COMMIT}@g" asset_register/settings.py

ENTRYPOINT ["/entrypoint"]
CMD ["gunicorn", "-c", "gunicorn.py", "asset_register.wsgi"]
