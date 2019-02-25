FROM python:3
LABEL description="This is Python image working for flask applications"
MAINTAINER Peter Holgersson <petersholgersson@gmail.com>
WORKDIR ./

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=shopping_app.py

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
