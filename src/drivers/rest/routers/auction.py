from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status

from drivers.rest.dependencies import get_submit_bid_use_case
from drivers.rest.routers.schema import BidInput
from use_cases.submit_bid_use_case import SubmitBidUseCase

router = APIRouter(prefix="/auctions")


@router.post("/{auction_id}/bids", status_code=status.HTTP_204_NO_CONTENT)
async def submit_bid(
    auction_id: UUID,
    data: BidInput,
    use_case: Annotated[SubmitBidUseCase, Depends(get_submit_bid_use_case)],
) -> None:
    await use_case(data.to_entity(auction_id))
