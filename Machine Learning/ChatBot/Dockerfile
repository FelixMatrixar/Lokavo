# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

RUN mkdir -p /gcp_service_account_keys

COPY /config/capstone-project-ents-h110-a6bf1280c72e.json /gcp_service_account_keys/

ENV GOOGLE_APPLICATION_CREDENTIALS=/gcp_service_account_keys/capstone-project-ents-h110-a6bf1280c72e.json

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5050

# Run app.py when the container launches
CMD ["gunicorn", "--bind", "0.0.0.0:5050", "app:app"]
