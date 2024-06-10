# Setup our environment

FROM python:3.10-alpine

WORKDIR /code

ENV PYTHONPATH=/code

# Copy our application code

COPY ./requirements.txt /code/requirements.txt

COPY ./alembic.ini /code/

COPY ./app /code/app

# Install our dependencies

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Start the application

CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]
