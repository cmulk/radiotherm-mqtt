FROM python:alpine
RUN apk add --no-cache  tzdata

ENV TZ America/Chicago

RUN pip install paho-mqtt radiotherm requests 

RUN mkdir -p /app

COPY radiotherm_translator.py /app
COPY myradiotherm.py /app

WORKDIR /app

CMD ["python3", "-u", "radiotherm_translator.py"]
