import socket

from fastapi import APIRouter
from fastapi import status

health_router = APIRouter()


@health_router.get("/health-check", status_code=status.HTTP_200_OK)
def health_check():
    return {
        "message": "OK",
        "version": "0.0.1",
        "hostname": socket.gethostname(),
    }
