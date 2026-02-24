.PHONY: run

# Start FastAPI dev server (no need to activate venv)
run:
	.venv/bin/python -m uvicorn main:app --reload
