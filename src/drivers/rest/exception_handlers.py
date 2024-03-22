from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from use_cases.exceptions import (
    AuctionNotActiveError,
    AuctionNotFoundError,
    LowBidError,
)
from adapters.exceptions import ExternalError


def exception_container(app: FastAPI) -> None:
    @app.exception_handler(AuctionNotFoundError)
    async def auction_not_found_exception_handler(
        request: Request, exc: AuctionNotFoundError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"message": str(exc)}
        )

    @app.exception_handler(AuctionNotActiveError)
    async def auction_not_active_exception_handler(
        request: Request, exc: AuctionNotActiveError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"message": str(exc)},
        )

    @app.exception_handler(LowBidError)
    async def low_bid_exception_handler(
        request: Request, exc: LowBidError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"message": str(exc)},
        )

    @app.exception_handler(ExternalError)
    async def external_exception_handler(
        request: Request, exc: ExternalError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Something went wrong. Please try again"},
        )
