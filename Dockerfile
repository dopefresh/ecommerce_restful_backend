FROM python:latest
WORKDIR /app
COPY . /app
RUN pip3 install poetry && poetry config virtualenvs.create false && poetry install --no-dev && poetry shell
ENV PYTHONPATH=${PYTHONPATH}:${PWD} 
