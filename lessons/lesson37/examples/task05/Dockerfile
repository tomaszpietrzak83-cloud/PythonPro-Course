FROM python:3.12 AS build
WORKDIR /build
COPY main.py .
RUN python -m compileall -b main.py
FROM python:3.12-slim
WORKDIR /app
COPY --from=build /build/main.pyc .
CMD ["python", "main.pyc"]
