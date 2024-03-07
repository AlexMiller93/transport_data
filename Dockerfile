FROM python:3.8-slim

WORKDIR /transport_data

COPY requirements.txt ./
RUN pip3 install --upgrade pip -r requirements.txt

COPY . /transport_data

EXPOSE 5473

CMD ["python3", "app.py"]