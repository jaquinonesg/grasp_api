FROM python:3.12 as python-base

# Configure Poetry
ENV POETRY_VERSION=1.6.1
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

FROM python-base as poetry-base

# Install poetry separated from system interpreter
RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

# Create a new stage from the base python image
FROM python-base as grasp-api-app

# Copy Poetry to app image
COPY --from=poetry-base ${POETRY_VENV} ${POETRY_VENV}

# Add Poetry to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"
WORKDIR /app
COPY . /app
COPY pyproject.toml .
COPY poetry.lock .
RUN poetry check
RUN poetry install --no-interaction --no-cache

EXPOSE 8000

CMD ["poetry", "run", "-m", "alembic", "upgrade", "head", "&&", "poetry", "run", "-m", "uvicorn", "grasp_api.api.app:uvicorn_entry", "--factory","--reload-include", "'src/**/*.py'","--reload", "--host=0.0.0.0", "--port=8000", "--log-level", "debug"]
