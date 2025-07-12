FROM python:3.13-slim
WORKDIR /app
COPY . /app
RUN pip install --upgrade pip && pip install -r requirements.txt
EXPOSE 12345
CMD ["python", "app.py"]
