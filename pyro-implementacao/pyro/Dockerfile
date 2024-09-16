FROM python:3.12

RUN apt-get update
# && apt-get install -y 

# COPY requirements.txt ./

RUN pip install --upgrade pip
RUN pip install Pyro5

CMD pyro5-ns
