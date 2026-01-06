FROM python:3-alpine

WORKDIR /app

RUN pip install poetry
COPY ./src ./
COPY ./pyproject.toml ./

RUN poetry install --no-root
CMD [ "poetry", "run", "python", "main.py" ]
