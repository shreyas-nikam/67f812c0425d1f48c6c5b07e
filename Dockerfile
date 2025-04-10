# Use Python base image
FROM python:3.12-slim

# Set working directory in the container
WORKDIR /app

# Copy requirements (adjust file name if needed)
COPY requirements.txt /app/

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application code
COPY . /app

# Set the port number via build-time or run-time environment (default is 8501)
ENV PORT=8501

# Expose the port so Docker maps it
EXPOSE $PORT

# Run Streamlit in headless mode
CMD ["bash", "-c", "streamlit run app.py --server.port=$PORT --server.headless=true"]
