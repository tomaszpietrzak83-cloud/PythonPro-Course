FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY tests tests
CMD ["python", "-m", "pytest", "-q"]
