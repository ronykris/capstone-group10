FROM python:3.8-slim

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /app
COPY app/ app/
RUN pip install uvicorn
RUN pip install fastapi
RUN pip install requests
RUN pip install python-multipart
RUN pip install prometheus_client
EXPOSE 8009

CMD ["uvicorn","app.main:app", "--host", "0.0.0.0", "--port", "8009"]
