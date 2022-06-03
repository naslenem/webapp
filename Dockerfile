FROM python:3

WORKDIR /usr/src/app

COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt

RUN pip3 install coverage

RUN useradd python-user

USER python-user

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8081"]
