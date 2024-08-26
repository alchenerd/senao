FROM python:3.12-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
VOLUME /app/data
EXPOSE 8000
CMD ["fastapi", "run", "main.py"]
