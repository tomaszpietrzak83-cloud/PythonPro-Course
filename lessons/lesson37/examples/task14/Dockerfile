FROM python:3.12-slim
WORKDIR /app
ENV PYTHONPATH=/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["django-admin", "runserver", "0.0.0.0:8000", "--settings=web", "--noreload"]
