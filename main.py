import os
from fastapi.responses import RedirectResponse
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import src.openAI.router as openAI
import src.langchainAPI.router as langchainRouter

app = FastAPI()
app.include_router(openAI.router)
app.include_router(langchainRouter.router)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def hello():
    return {"message": "Hello World"}


@app.exception_handler(404)
async def custom_404_handler(_, __):
    return RedirectResponse("/")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
