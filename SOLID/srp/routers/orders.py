from fastapi import APIRouter, HTTPException, status
from services import order_service
from services.order_service import OrderNotFoundError

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/")
def create_order(order_data: dict):
    try:
        order = order_service.create_order(order_data)
        return order
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.patch("/{order_id}/status")
def update_order_status(order_id: int, new_status: dict):
    try:
        order = order_service.update_order(
            order_id,
            new_status["status"]
        )
        return order
    except OrderNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )