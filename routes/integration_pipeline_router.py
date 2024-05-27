from fastapi import APIRouter, Request, Response, status
import logging
from aidbox.base import API
import traceback
import json

from HL7v2.ORU import R01
from HL7v2.VXU import V04


router = APIRouter()
logger = logging.getLogger("log")


async def convert_message(message):
    response = API.do_request(
        endpoint="/hl7in/ADT", method="POST", json={"message": message}
    )
    response.raise_for_status()
    return response.json()


async def request_wrapper(raw_data, action):
    try:
        parsed_data = await convert_message(raw_data.decode("utf-8"))
        action(parsed_data["parsed"]["parsed"])
        response = {"message": "DONE"}
        return response
    except Exception as e:
        response = json.dumps({'error': str(e)}).encode('utf-8')
        logger.error("Unable to add the record: %s" % response)
        logger.error(traceback.format_exc())
        return Response(content=response, status_code=status.HTTP_400_BAD_REQUEST)


@router.post("/ORU_R01")
async def hl7v2_oru_r01(request: Request):
    raw_data = await request.body()
    logger.info("raw_data: %s" % raw_data)
    return await request_wrapper(raw_data, R01.run)


@router.post("/VXU_V04")
async def hl7v2_vxu_v04(request: Request):
    raw_data = await request.body()
    logger.info("raw_data: %s" % raw_data)
    response = await request_wrapper(raw_data, V04.run)
    return response
