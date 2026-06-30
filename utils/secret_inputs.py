import os


def effective_secret(user_value: str | None, env_name: str) -> str:
    """Return a typed secret, or fall back to an environment secret."""
    return (user_value or "").strip() or os.getenv(env_name, "")
