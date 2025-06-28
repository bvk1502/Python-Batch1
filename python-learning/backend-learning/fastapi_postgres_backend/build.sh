#!/bin/bash
export PYTHONPATH=.
set -a
source .env
set +a
alembic upgrade head
python -c "import asyncio; from app.db.session import async_session; from app.db.init_db import init_db; asyncio.run(init_db(async_session()))"
