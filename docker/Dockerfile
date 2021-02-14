FROM python:3.8.3-slim-buster

# Set the working directory
RUN mkdir -p /app
WORKDIR /app

# Deactivate some unneeded python features
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system deps
RUN apt-get update && apt-get upgrade -y && apt-get install git texlive texlive-extra-utils poppler-utils netpbm -y

# Install the package manager
RUN pip install 'poetry>=1.0'

# Clone repository
RUN git clone https://e6e2acbb32553d41c4454ab99f670e5005e4dcef@github.com/LeGmask/ShoutBot.git ./


# Install stuff
RUN poetry install

