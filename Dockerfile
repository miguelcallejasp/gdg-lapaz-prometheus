FROM python:3.6.12-alpine

WORKDIR /
COPY requirements.txt /
RUN pip3 install -r requirements.txt
COPY . .
ENV PYTHONPATH=/

ENTRYPOINT ["python3"]
CMD ["/app.py"]
