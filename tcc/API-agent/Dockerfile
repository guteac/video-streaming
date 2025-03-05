FROM python:3.10

WORKDIR /usr

COPY config .

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

WORKDIR /usr/src

COPY src/main.py .

# Command to start FastAPI server using Uvicorn
CMD ["fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]