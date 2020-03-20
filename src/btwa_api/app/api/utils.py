from fastapi import HTTPException


def get_or_404(value, detail=None):
    if value is None:
        raise HTTPException(status_code=404, detail=detail)
    return value
