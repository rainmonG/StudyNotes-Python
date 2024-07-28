"""
@Time : 2024-07-28 22:08
@Author : rainmon
@File : fast_server.py
@Project : StudyNotes-Python
@feature : 
@description：
"""
import uvicorn
from fastapi import FastAPI

from fast_router import router


app = FastAPI()
app.include_router(router)


if __name__ == '__main__':
    uvicorn.run("fast_server:app", reload=True, port=8345)
