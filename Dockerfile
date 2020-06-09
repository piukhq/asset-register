FROM python:3.8-slim
ARG COMMIT="GITHASH"

WORKDIR /app
COPY poetry.lock pyproject.toml /app/

RUN pip install --no-cache-dir poetry psycopg2-binary && \
    poetry config virtualenvs.create false --local
RUN poetry install --no-dev --no-root

COPY asset_register /app/asset_register/

WORKDIR /app/asset_register
RUN sed -i "s@__VERSION__@$(date +%Y-%m-%dT%H:%M:%S-)${COMMIT}@g" asset_register/settings.py

CMD ["gunicorn", "-c", "gunicorn.py", "asset_register.wsgi"]
