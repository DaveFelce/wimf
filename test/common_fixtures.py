import pytest
from recipes.documents import RecipeDocument


@pytest.fixture()
def clear_recipe_index():
    """
    Ensure the recipes index is cleared down before and after every test
    """
    RecipeDocument._index.delete(ignore=[404])
    yield
    RecipeDocument._index.delete(ignore=[404])
