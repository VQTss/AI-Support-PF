from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from loguru import logger
from utils import llm_summary_chatGPT , analysis_counter
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import pandas as pd
from io import BytesIO
import asyncio
from concurrent.futures import ThreadPoolExecutor
from fastapi.responses import StreamingResponse
app = FastAPI()

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

@app.post("/chatGPT-solution")
async def chat(
    user_input: str,
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],

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
    response = llm_summary_chatGPT(user_input=user_input,condition=False)
    return {"response": response}


# Define a function to run the analysis in a thread pool
async def run_analysis_in_threadpool(file: UploadFile):
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        output = await loop.run_in_executor(pool, analysis_counter, file.file)
    return output


@app.post("/analyze_excel")
async def analyze_excel(file: UploadFile = File(...)):
    # Read file content into memory
    file_content = await file.read()
    
    # Run the analysis on the file content
    output =  analysis_counter(file_content)

    # Return the Excel file directly using StreamingResponse
    return StreamingResponse(output, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": f"attachment; filename=analysis_{file.filename}"})

