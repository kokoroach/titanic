from fastapi import APIRouter

from app.application.cache import delete_keys_having_prefix

router = APIRouter()


@router.get("/reset-cache", status_code=200)
async def reset_cache():
    # TODO: Delete all not just passenger prefix
    await delete_keys_having_prefix(prefix="passenger")

    return "Cache has been reset."
