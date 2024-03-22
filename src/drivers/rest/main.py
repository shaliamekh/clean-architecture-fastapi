from fastapi import FastAPI

from drivers.rest.exception_handlers import exception_container
from drivers.rest.routers import auction

app = FastAPI()

app.include_router(auction.router)

exception_container(app)
