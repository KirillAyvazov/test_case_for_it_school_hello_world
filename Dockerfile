FROM python:3.11-slim-bullseye

WORKDIR /app

COPY ./src ./src
COPY ./test ./test
COPY ./.env ./.env
COPY ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r ./requirements.txt

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
