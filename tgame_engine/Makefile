lint:
	poetry run flake8
run:
	poetry run gunicorn app:app --bind 0.0.0.0:5000 -w 4 -k uvicorn.workers.UvicornWorker