lint:
	poetry run flake8
run:
	poetry run gunicorn app:app  -w 4 -k uvicorn.workers.UvicornWorker