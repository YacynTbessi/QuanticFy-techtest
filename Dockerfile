# Use the official Python image as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the application files into the container
COPY app.py .
COPY setup_db.py .

# Install the required dependencies
RUN pip install pandas requests dash plotly db-sqlite3

# Run setup_db.py to create the SQLite database
RUN python setup_db.py

# Expose the port that Dash will run on
EXPOSE 8081

# Command to run your application
CMD ["python", "app.py"]
