import pytest
from tcg_portfolio import calculate_portfolio_value, generate_card_html, extract_price

def test_calculate_portfolio_value():
    """Verify that the portfolio calculator sums correctly."""
    # Scenario 1: Standard list of cards
    cards = [
        {"name": "Card A", "market_price": 10.50},
        {"name": "Card B", "market_price": 5.25},
        {"name": "Card C", "market_price": 4.25}
    ]
    # 10.50 + 5.25 + 4.25 = 20.00
    assert calculate_portfolio_value(cards) == 20.00

    # Scenario 2: Empty list (Should be 0)
    assert calculate_portfolio_value([]) == 0.0

    # Scenario 3: Zero value cards
    cards_zero = [{"name": "Fake Card", "market_price": 0.0}]
    assert calculate_portfolio_value(cards_zero) == 0.0

def test_extract_price():
    """Verify JSON parsing logic works on fake API data."""
    # Scenario 1: Holofoil price exists (Preferred)
    api_response_holo = {
        "tcgplayer": {
            "prices": {
                "holofoil": {"market": 150.0},
                "normal": {"market": 10.0}
            }
        }
    }
    assert extract_price(api_response_holo) == 150.0

    # Scenario 2: Only Normal price exists
    api_response_normal = {
        "tcgplayer": {
            "prices": {
                "normal": {"market": 5.0}
            }
        }
    }
    assert extract_price(api_response_normal) == 5.0

    # Scenario 3: No price data at all
    assert extract_price({}) == 0.0

def test_generate_card_html():
    """Verify that HTML string contains the correct data."""
    fake_card = {
        "name": "Test Charizard",
        # FIX: Added the missing 'set' key here
        "set": "Test Base Set",
        "image": "http://example.com/charizard.png",
        "market_price": 100.00
    }
    
    result = generate_card_html(fake_card)
    
    # Assert that key pieces of data are inside the string
    assert "Test Charizard" in result
    assert "Test Base Set" in result
    assert "100.00" in result
    assert "http://example.com/charizard.png" in result
    assert "card-item" in result

