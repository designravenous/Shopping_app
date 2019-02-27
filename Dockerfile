FROM python:3
LABEL description="This is Python image working for flask applications"
MAINTAINER Peter Holgersson <petersholgersson@gmail.com>

RUN groupadd -g 999 appuser && \
    useradd -r -u 999 -g appuser appuser
USER appuser


COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt --user

COPY . .

ENV FLASK_APP=shopping_app.py 

RUN chmod 777 app.db

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
