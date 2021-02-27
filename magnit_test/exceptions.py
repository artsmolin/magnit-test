class EmptyBody(Exception):
    def __str__(self) -> str:
        return "Body is required"
