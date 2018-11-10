# Use an official Python runtime as a parent image
FROM python:3.7.1

# Set the working directory to /container
WORKDIR /app_container

# Copy the current directory contents into the container at /app
COPY . /app_container

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "Commuter_App.py"]