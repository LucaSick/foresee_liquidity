FROM python:3.9

RUN apt-get update
RUN apt-get install -y --no-install-recommends \
    python3-pip \
    python3-dev


RUN mkdir /foresee-liquidity
COPY ./requirements.txt /foresee-liquidity/requirements.txt
WORKDIR /foresee-liquidity
RUN pip install -r requirements.txt
COPY . /foresee-liquidity
EXPOSE 8080
CMD python src/kucoin_socket.py
