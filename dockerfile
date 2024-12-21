FROM python

WORKDIR /home

EXPOSE 8000

COPY ./server.py .
COPY ./requirements.txt .

RUN pip3 install -r /home/requirements.txt

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
