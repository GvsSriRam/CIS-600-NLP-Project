"""Module providing endpoint routes for backend application"""
from fastapi import APIRouter

from log import logger
from api.model_connector import ModelConnector


# Contains endpoints that are exposed externally
router = APIRouter()

model_connector_obj = ModelConnector()

# Endpoint to train the model
@router.get("/train", tags=["split"])
def train_model():
    """
    Endpoint to trigger model training.
    
    Returns:
        dict: Training result indicating success or failure.
    """
    result = {"success": False, "error": ""}
    try:
        # Trigger model training
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

# Endpoint to chat with the model
@router.post("/chat", tags=["split"])
def chat(params: dict):
    """
    Endpoint for interacting with the model.
    
    Args:
        params (dict): Input parameters containing the text to be processed.
    
    Returns:
        dict: Result of the chat operation.
    """
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
