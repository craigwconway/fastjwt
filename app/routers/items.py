from fastapi import APIRouter, Depends, HTTPException


router = APIRouter(
    prefix="/items",
    tags=["items"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
def read_items():
    return []  # TODO


@router.get("/{item_id}")
def read_item(item_id: str):
    if item_id not in []:
        raise HTTPException(status_code=404, detail="Item not found")
    return []


@router.put("/{item_id}")
def update_item(item_id: str):
    if item_id != "1":
        raise HTTPException(status_code=403, detail="Um yeah")
    return []
