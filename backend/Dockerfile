FROM python:3.11

WORKDIR /app
COPY . backend
RUN pip install --upgrade pip
RUN pip install -r backend/requirements.txt --no-cache-dir
CMD ["python", "-m", "backend.main"]