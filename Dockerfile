FROM python:3.12-alpine

RUN adduser --disabled-password --gecos '' offerAdmin
WORKDIR /opt/

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN chown -R offerAdmin:offerAdmin .
RUN mkdir -p /static && chown -R offerAdmin:offerAdmin /static
RUN mkdir -p /media && chown -R offerAdmin:offerAdmin /media

USER offerAdmin

ENV PATH opt/.venv/bin:$PATH

EXPOSE 8000
