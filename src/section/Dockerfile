FROM python:3.7.6-alpine

COPY . /app
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt \
  && adduser -D appuser \
  && chown -R appuser:appuser /app

USER appuser

EXPOSE 8080

ENTRYPOINT ["python"]
CMD ["main.py"]