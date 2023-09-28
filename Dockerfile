FROM python:3.11.5-slim

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN python -m pip install --no-cache-dir poetry==1.6.1 \
    && poetry config virtualenvs.create false \
    && poetry install --without code,tests --no-interaction --no-ansi -vvv\
    && rm -rf $(poetry config cache-dir)/{cache, artifacts}

COPY . .

CMD alembic upgrade head && uvicorn src.main:main_app --host=0.0.0.0 --port=80
