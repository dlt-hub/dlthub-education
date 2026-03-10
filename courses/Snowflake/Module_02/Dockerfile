FROM python:3.11-slim

# Set Python to run in unbuffered mode so logs appear immediately
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy all project files
COPY ./ /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# When container launches, run the pipeline script
CMD ["python", "-u", "github_api_pipeline.py"]