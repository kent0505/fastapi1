from fastapi             import APIRouter, Depends
from app.auth.jwt_bearer import JwtBearer
import logging


# router = APIRouter()
router = APIRouter(dependencies=[Depends(JwtBearer())])


@router.get("/last")
async def get_last_logs():
    logging.info("GET 200 /logs/last/")

    with open("logfile.log", "r") as file:
        lines = file.readlines()
        line_count = len(lines)

    return {
        "lines": line_count,
        "logs":  lines[-100:]
    }


@router.get("/delete")
async def delete_logs():
    with open("logfile.log", "w"):
        pass

    logging.info("GET 200 /logs/delete/")
    return {"message": "logs deleted"}


# @router.get("/data/{aa}/{bb}")
# async def get_logs(aa: int, bb: int):
#     logging.info(f"GET 200 /logs/data/{aa}/{bb}/")

#     with open("logfile.log", "r") as file:
#         lines = file.readlines()

#     return {"logs": lines[aa:bb]}


# @router.get("/lines")
# async def get_lines():
#     logging.info("GET 200 /logs/lines/")

#     with open("logfile.log", "r") as file:
#         lines = file.readlines()
#         line_count = len(lines)

#     return {"log_lines": f"{line_count}"}