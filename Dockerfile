# Start from an official, lightweight Python image
FROM python:3.11-slim

# All following commands run inside that image
WORKDIR /app                    # create /app and cd into it

# Install dependencies first (keeps rebuilds fast)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of Pantrify’s code
COPY . .

# Launch FastAPI with Uvicorn on port 8080 (the port App Runner expects)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
