FROM python:3.7
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt /app
RUN pip install --upgrade pip 
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
EXPOSE 8000
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]