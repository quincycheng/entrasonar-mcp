FROM python:3.12

WORKDIR /app

# Configure environmental controls specifically for port 8000
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000 \
    FASTMCP_STATELESS_HTTP=true

# Add metadata labels for Docker Hub
LABEL maintainer="Quincy Cheng <quincy@example.com>"
LABEL description="EntraSonar MCP - Microsoft Entra ID and Azure infrastructure reconnaissance server"
LABEL version="0.1.0"
LABEL org.opencontainers.image.source="https://github.com/your-org/entrasonar-mcp"

# Pull in your dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy over the clean FastMCP script context
COPY main.py .

# Expose port 8000 to comply with the AgentCore protocol contract
EXPOSE 8000

# Execute natively using Python
CMD ["python", "main.py"]