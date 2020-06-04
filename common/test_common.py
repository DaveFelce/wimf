from django.test import TestCase
from common.utils import (
    cleanup_ingredients,
    lc_whitespaced_str_of_ingredients,
    lc_csv_str_of_ingredients,
    sorted_ingredients_as_csv,
    split_csv_into_list,
)


class TestUtils(TestCase):
    """ Test common utils """

    def setUp(self):
        self.ingredients_with_mixed_chars = (
            "\"%%% one.  .. & ^ ^^( thing) **** *%   % $£ !\",  two, 'three',four***"
        )

    def test_ingredients_cleanup(self):
        """
        Test the removal of non-word and extra spaces from ingredients keywords
        """

        # GIVEN
        ingredients = "\"one. thing\",  two, 'three',four"
        ingredients2 = '"""one. \'  thing",  " ;;;;  ,,  ;, ; . two, :\'three\',four:";'
        expected_ingredient_keywords = "one thing two three four"

        # THEN
        assert cleanup_ingredients(ingredients) == expected_ingredient_keywords
        assert cleanup_ingredients(self.ingredients_with_mixed_chars) == expected_ingredient_keywords
        assert cleanup_ingredients(ingredients2) == expected_ingredient_keywords

    def test_lc_whitespaced_str_of_ingredients(self):
        """
        Test the creation of a lowercased list of ingredients keywords
        """

        # GIVEN
        ingredients_multiple_space_str = "one  thing   two     three four"
        ingredients_single_spaced_str = "one thing two three four"
        expected_ingredient_keywords_list = ["one", "thing", "two", "three", "four"]

        # THEN
        assert lc_whitespaced_str_of_ingredients(self.ingredients_with_mixed_chars) == expected_ingredient_keywords_list
        assert lc_whitespaced_str_of_ingredients(ingredients_multiple_space_str) == expected_ingredient_keywords_list
        assert lc_whitespaced_str_of_ingredients(ingredients_single_spaced_str) == expected_ingredient_keywords_list

    def test_lc_csv_str_of_ingredients(self):
        """
        Test the creation of a lowercased list of CSV ingredients keywords
        """

        # GIVEN
        ingredients_csv_str = "One, Thing, TWO, thREE, fOUR"
        expected_ingredient_list = ["one", "thing", "two", "three", "four"]

        # THEN
        assert lc_csv_str_of_ingredients(ingredients_csv_str) == expected_ingredient_list

    def test_sorted_ingredients_as_csv(self):
        """
        Test the creation of a lowercased, sorted csv string from unsorted csv string
        """

        # GIVEN
        ingredients_csv_str = "One, Thing, TWO, thREE, fOUR"
        expected_ingredients_string = "four, one, thing, three, two"

        # WHEN
        sorted_ingredients = sorted_ingredients_as_csv(ingredients_csv_str)

        # THEN
        assert sorted_ingredients == expected_ingredients_string

    def test_split_csv_into_list(self):
        """ Test splitting csv string into a list """

        # GIVEN
        expected_ingredients_list = [
            "ground beef",
            "cumin",
            "tomatoes",
            "cheese",
            "ground black pepper",
        ]
        ingredients_str = "ground beef, cumin, tomatoes, cheese, ground black pepper"

        # THEN
        assert split_csv_into_list(ingredients_str) == expected_ingredients_list
