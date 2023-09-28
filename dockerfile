FROM python:3.8

COPY app.py model.pkl preprocessor.pkl requirements.txt inflamation_features.py /app/
COPY templates /app/templates

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

ENV UVICORN_CMD="uvicorn app:app --host 0.0.0.0 --port 80 --workers 4 --reload"

EXPOSE 80

CMD ["sh", "-c", "$UVICORN_CMD"]