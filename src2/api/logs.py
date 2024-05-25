from fastapi         import APIRouter
from src.core.config import settings


router = APIRouter()


@router.get("/last")
async def get_last_logs():
    with open(settings.log_filename, "r") as file:
        lines = file.readlines()
        count = len(lines)

    new_lines = []

    for line in lines:
        new_lines.append(line.strip())

    return {
        "lines": count,
        "logs":  new_lines[-1000:]
    }


@router.get("/delete")
async def delete_logs():
    with open(settings.log_filename, "w"):
        pass

    return {"message": "logs deleted"}