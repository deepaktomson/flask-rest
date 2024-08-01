FROM python:3.10-alpine3.20

WORKDIR /home/flask/app

COPY . .

RUN pip install flask

CMD ["flask", "run", "--host", "0.0.0.0"]