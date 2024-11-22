import asyncio
import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
from data.data_fetcher import *
from util.common import *
from util.options_position import *

@pytest.mark.asyncio
async def test_get_security_closing_price():
    ticker = "NVDA"
    date = "2024-11-15"

    # NVDA closed at 141.98 on 2024-11-15
    assert await get_security_closing_price(ticker, date) == 141.98
