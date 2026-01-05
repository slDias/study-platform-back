FROM python:3-alpine

WORKDIR /app

RUN pip install poetry
RUN poetry install

COPY ./src ./
CMD [ "python", "main.py" ]
