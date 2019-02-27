FROM python:3

WORKDIR ./

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=shopping_app.py
EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]
