FROM python:3.10

RUN apt-get update
# # && apt-get install -y 

COPY requirements.txt ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD python3 -u server.py