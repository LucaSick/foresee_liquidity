FROM python:3.8

RUN apt-get update
RUN apt-get install -y --no-install-recommends \
    python3-pip \
    python3-dev \
    postgresql-server-dev-all


RUN psql
# RUN psql -c "CREATE USER market WITH SUPERUSER PASSWORD '12345';"
# RUN psql -c "CREATE DATABASE market_db;"


RUN mkdir /foresee-liquidity
COPY ./requirements.txt /foresee-liquidity/requirements.txt
WORKDIR /foresee-liquidity
RUN pip install -r requirements.txt
COPY . /foresee-liquidity
EXPOSE 8080
CMD ["python", "src/kucoin_socket.py"]