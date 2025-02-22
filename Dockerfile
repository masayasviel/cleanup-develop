FROM python
WORKDIR /app/src
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r /app/requirements.txt
COPY . /app/
