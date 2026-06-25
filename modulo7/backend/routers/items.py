from fastapi import APIRouter, status
from models.items import CreateItem, ItemResponse

router = APIRouter(prefix="/public", tags=["Items"])

items_db = [
    {
        "id": 1,
        "name": "Item 1",
        "description": "Descripción del item 1"
    },
    {
        "id": 2,
        "name": "Item 2",
        "description": "Descripción del item 2"
    },
    {
        "id": 3,
        "name": "Item 3",
        "description": "Descripción del item 3"
    }
]

@router.get("/items")
def get_items():
    return items_db

# Create item
@router.post("/items", response_model= ItemResponse, status_code= status.HTTP_201_CREATED)
def create_item(item: CreateItem):
    new_id = max(i["id"] for i in items_db) + 1

    item_data = item.model_dump()
    item_data["id"] = new_id

    items_db.append(item_data)

    return item_data