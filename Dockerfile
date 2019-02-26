FROM python:3
LABEL description="This is Python image working for flask applications"
MAINTAINER Peter Holgersson <petersholgersson@gmail.com>
USER sqlite
WORKDIR ./

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=shopping_app.py 

RUN chmod 777 app.db

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
