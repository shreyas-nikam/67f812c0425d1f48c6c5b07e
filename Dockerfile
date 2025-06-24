
# Use Python base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the application code
COPY . /app

# Set default port and expose it
ENV PORT=8501
EXPOSE $PORT

# Run the Streamlit application
CMD [ "bash", "-c", "streamlit run app.py --server.port=$PORT --server.headless=true" ]
