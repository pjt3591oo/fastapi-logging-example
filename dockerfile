FROM python:3.10-alpine

COPY ./ /var/app
WORKDIR /var/app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt

EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--workers", "3", "--log-config", "log.ini"]