import json
import logging
from apps.recipes.documents import RecipeDocument

# Get an instance of a logger
logger = logging.getLogger(__name__)


def get_recipes_from_search(es_search):
    """
    Populate a dict with hit results foreach hit returned by Elasticsearch.  Push onto list and return.

    Params:
        The ES search obj

    Returns:
        recipes list of dicts(.. of hit results)
    """
    recipes = []
    for hit in es_search:
        recipes.append(
            {
                "id": hit.id,
                "ingredients": hit.ingredients,
                "name": hit.name,
                "score": hit.meta.score,
                "url": hit.url,
            }
        )

    return recipes


class RecipeSearch:
    """
    Carry out the Elasticsearch query and return results
    """

    def do_search(self, search_params):
        """ Do the actual search, using the search params we've been passed

        Params: 
            search_params(dict):
            'ingredients': str of space delimited keywords
        """
        es_search = RecipeDocument.search().query(
            "match", ingredients=search_params["ingredients"]
        )

        # Log the query_params and JSON query used
        logger.debug(json.dumps(search_params))
        logger.debug(json.dumps(es_search.to_dict()))

        results = get_recipes_from_search(es_search)
        return results
