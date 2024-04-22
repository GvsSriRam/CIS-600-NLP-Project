
from fastapi import APIRouter, File, UploadFile

from log import logger
from api.model_connector import ModelConnector


# Contains End_Points that are exposed externally

router = APIRouter()

model_connector_obj = ModelConnector()


@router.get("/train", tags=["split"])
def train_model():
    result = {"success": False, "error": ""}
    try:
        error = model_connector_obj.train()
        if error:
            result["success"] = False
            result["error"] = error
        else:
            result["success"] = True
    except Exception as e:
        logger.error(str(e))
        result["error"] = str(e)
    return result

@router.post("/chat", tags=["split"])
def chat(params: dict):
    input_str = params.get("input")
    result = {
                "success": False, 
                "result": None, 
                "error": ""
            }
    try:
        result["result"], result["error"] = model_connector_obj.q_a(input_str)
        if not result["error"]:
            result["success"] = True
    except Exception as e:
        logger.error(str(e))
        result["error"] = str(e)
    return result
