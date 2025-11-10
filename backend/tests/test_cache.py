"""
Can only be ran when redis-client is running

Ideally use Mock operation for offline check, where possible
"""

import pytest

from backend.app.core.cache import (
    close_redis,
    delete_keys_having_prefix,
    get_data_from_cache,
    init_redis,
    set_cache_data,
)


@pytest.mark.asyncio
async def test_redis_cache_operations():
    await init_redis()

    # Test set_cache_data and get_data_from_cache
    await set_cache_data("test_key", {"a": 1})
    cached = await get_data_from_cache("test_key")
    assert cached == {"a": 1}

    # Test delete_keys_having_prefix
    await delete_keys_having_prefix("test_")
    cached = await get_data_from_cache("test_key")
    assert cached is None

    await close_redis()
