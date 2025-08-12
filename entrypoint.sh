#!/bin/sh

alembic upgrade head
exec uvicorn lib.main:app --host 0.0.0.0 --port 8000 --reload