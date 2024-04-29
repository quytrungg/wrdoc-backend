def get_test_file_url(path: str) -> str:
    """Add localhost to relative URI."""
    if path.startswith("/"):
        return f"http://localhost:8000{path}"
    return f"http://localhost:8000/{path}"
