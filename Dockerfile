FROM python:3.8-slim

WORKDIR /app
COPY poetry.lock pyproject.toml /app/

RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false --local && \
    poetry install

COPY asset_register /app/asset_register/

WORKDIR /app/asset_register

CMD ["gunicorn", "-c", "gunicorn.py", "asset_register.wsgi"]
