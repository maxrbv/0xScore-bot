FROM python:3.10

COPY ./ /app/

WORKDIR /app

RUN pip install -r requirements.txt

WORKDIR /app

CMD ["sh", "-c", "python app.py & python updater.py"]