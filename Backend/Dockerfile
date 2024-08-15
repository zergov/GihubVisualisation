FROM python:3-slim

WORKDIR /code

COPY ./resources/. /code/resources/
RUN apt-get update && apt-get install -y git
RUN pip install --no-cache-dir --upgrade -r /code/resources/requirements.txt
RUN pip install "fastapi[standard]"
COPY ./cache /code/cache
COPY ./api /code/api

CMD ["fastapi", "run", "api/main.py", "--port", "80"]