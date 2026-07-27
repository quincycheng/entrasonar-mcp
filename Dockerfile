FROM python:3.12-slim

WORKDIR /app

# Configure environmental controls specifically for port 8000
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000 \
    FASTMCP_STATELESS_HTTP=true

# Pull in your stripped-down dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy over the clean FastMCP script context
COPY main.py .

# Expose port 8000 to comply with the AgentCore protocol contract
EXPOSE 8000

# Execute natively using Python
CMD ["python", "main.py"]