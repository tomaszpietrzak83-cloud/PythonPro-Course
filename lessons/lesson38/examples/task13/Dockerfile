FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY tests tests
COPY src src
COPY pyproject.toml .
CMD ["python", "-m", "pytest", "-q"]
