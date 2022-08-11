# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.9-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./
RUN python3 -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt


CMD ["python3", "main.py"]