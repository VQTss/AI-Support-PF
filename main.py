from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from loguru import logger

from utils import llm_summary_chatGPT


app = FastAPI()
security = HTTPBasic()


@app.post("/chatGPT")
async def chat(
    user_input: str,
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
    openAIKey=None, 
    model_llm= None, 
    prompt_model=None,
):
    # tránh truy cập bất hợp pháp
    if credentials.username != "bbuser" or credentials.password != "1234":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    if user_input is None:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="User input is empty! Please enter again.",
            headers={'Content-Type': 'application/json'}
        )
    # logger.info()
    response = llm_summary_chatGPT(user_input=user_input,openAIKey=openAIKey,model_llm=model_llm,prompt_model=prompt_model)
    return {"response": response}
