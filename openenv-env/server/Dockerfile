FROM python:3.12-slim

WORKDIR /app
# The environment lives in the outcome-evals package; this folder is the OpenEnv wrapper.
RUN pip install --no-cache-dir "outcome-evals[openenv] @ https://github.com/palanorinc/outcome-evals/archive/refs/heads/main.zip"
COPY . /app
ENV OUTCOME_EVALS_SPLIT=resolved_history
EXPOSE 8000
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "8000"]
