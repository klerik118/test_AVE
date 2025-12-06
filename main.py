from fastapi import FastAPI

from app.routers import router


app = FastAPI(title="telephone-address")


@app.get('/health')
async def welcome():
    return 'Welcom to telephone-address!'


app.include_router(router)