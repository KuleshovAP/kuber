FROM python:3.11.11-slim-bookworm
WORKDIR /app
COPY app/requirements.txt app/requirements.txt
RUN pip install --no-cache-dir -r app/requirements.txt
COPY app/ app/
COPY tests/ tests/
ENV PYTHONUNBUFFERED=1
CMD ["python", "-m", "app.main"]
