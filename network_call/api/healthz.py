# Ping - Pong to check which IP it'll be using ( WiFi or Ethernet )

# FastAPI Imports
from fastapi import APIRouter, status, Response


router = APIRouter(prefix="/healthz", tags=["Healthz"])


@router.get("/ping")
async def get_ping():
    return Response(
        status_code=status.HTTP_200_OK,
        content="PONG",
    )
