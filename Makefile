dev:
	uv run uvicorn app.main:app --reload

worker:
	PYTHONPATH=. python -m app.workers.views_worker