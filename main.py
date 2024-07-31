from fastapi import FastAPI
from routes.route import router
from mangum import Mangum

app=FastAPI()
handler=Mangum(app)

app.include_router(router)