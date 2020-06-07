import pytest


@pytest.fixture()
def test_recipe():
    """
    A test recipe dict
    """
    test_recipe = {
        "name": "Three In One Onion Dip Recipe",
        "url": "http://cookeatshare.com/recipes/three-in-one-onion-dip-4122",
        "ingredients": "cheddar cheese, cheese, green onion",
    }

    yield test_recipe
