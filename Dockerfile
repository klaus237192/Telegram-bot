FROM python:3.9-slim-buster
LABEL Author="davidson"
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --upgrade pip 
RUN apt-get update && \
    apt-get install -y gcc python3-tk python3-dev libssl-dev libffi-dev build-essential

RUN pip install --no-cache-dir -r requirements.txt

COPY main.py handler.py config.py captureutil.py database.py tradingview.py ./
EXPOSE 80

ENTRYPOINT [ "python", "main.py" ]