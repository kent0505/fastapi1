from fastapi   import APIRouter
from src.utils import *


router = APIRouter()


@router.get("/last")
async def get_last_logs():
    with open("logfile.log", "r") as file:
        lines = file.readlines()
        line_count = len(lines)

    new_lines = []

    for line in lines:
        new_lines.append(line.strip())

    return {
        "lines": line_count,
        "logs":  new_lines[-1000:]
    }


@router.get("/delete")
async def delete_logs():
    with open("logfile.log", "w"):
        pass

    return {"message": "logs deleted"}