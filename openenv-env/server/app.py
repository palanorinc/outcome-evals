"""OpenEnv entry point: the FastAPI app from outcome_evals."""

from outcome_evals.adapters.openenv_server import app, main

__all__ = ["app", "main"]

if __name__ == "__main__":
    main()
