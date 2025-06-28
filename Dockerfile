# Use a standard Python 3.9 image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /code

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port Hugging Face expects
EXPOSE 7860

# Command to run the application using a production server
# This is the NEW, corrected line with the timeout increase
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "--timeout", "120", "app:app"]