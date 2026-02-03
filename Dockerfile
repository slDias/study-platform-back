FROM python:3-alpine

WORKDIR /app

RUN pip install poetry
COPY ./src/**/*.py ./
RUN rm -rf ./tests
COPY ./pyproject.toml ./
COPY ./poetry.lock ./

RUN poetry install --no-root
CMD [ "poetry", "run", "python", "main.py" ]
