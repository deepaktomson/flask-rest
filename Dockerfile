FROM python:3.10-alpine3.20

WORKDIR /home/flask/app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["flask", "run", "--host", "0.0.0.0"]