FROM python:3
RUN python3 -m pip install gunicorn flask
COPY ./app /app
ENV PYTHONUNBUFFERED 1
ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:8000", "--workers", "2", "--threads", "2",  "app.app:app"]