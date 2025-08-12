FROM python:3.13-slim

WORKDIR /app

COPY . .

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000

# CMD ["uvicorn", "lib.main:app", "--host", "0.0.0.0", "--port", "8000"]

CMD ["/entrypoint.sh"]