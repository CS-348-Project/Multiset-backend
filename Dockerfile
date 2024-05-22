# Use an official Python image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/

RUN apt-get update && apt-get install -y gcc libpq-dev
RUN pip install --no-cache-dir -r requirements.txt

# Copy the DjangoNinja app
COPY . /app/

EXPOSE 8000

# Command to run the Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]