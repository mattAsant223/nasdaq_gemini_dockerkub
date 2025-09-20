

FROM python:3.9-alpine AS builder

WORKDIR /usr/src/app

RUN apk add --no-cache build-base

COPY requirements.txt ./
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt


FROM python:3.9-alpine


RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

WORKDIR /home/appuser/app


COPY --from=builder /opt/venv /opt/venv


COPY ./app ./app
COPY ./run.py .


ENV PATH="/opt/venv/bin:$PATH"


EXPOSE 5000


CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]