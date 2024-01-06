from fastapi             import APIRouter, Depends
from app.auth.jwt_bearer import JwtBearer
import logging


router = APIRouter()
# router = APIRouter(dependencies=[Depends(JwtBearer())])


@router.get("/data/{aa}/{bb}")
async def convert(aa: int, bb: int):
    logging.info("GET 200 /logs/convert/")

    with open('logfile.log', 'r') as file:
        lines = file.readlines()

    return {"logs": lines[aa:bb]}


@router.get("/lines")
async def convert():
    logging.info("GET 200 /logs/convert/")

    with open('logfile.log', 'r') as file:
        lines = file.readlines()
        line_count = len(lines)

    return {"logs": f"{line_count}"}


@router.get("/delete")
async def delete_logs():
    with open('logfile.log', 'w'):
        pass

    logging.info("GET 200 /logs/delete/")
    return {"message": "logs deleted"}