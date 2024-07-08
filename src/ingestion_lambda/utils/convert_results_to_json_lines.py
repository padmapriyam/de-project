import json
import datetime
from decimal import Decimal


def convert_dict_to_json(d: dict) -> str:
    """Converts a Python dictionary to a JSON formatted string.

    Before serialisation, any values that are datetime objects are converted
    to strings in ISO 8601 format, and any that are Decimal objects are
    converted to float.

    Args:
        d: A dictionary whose values are expected to be JSON serialisable, or
          datetime.datetime objects or decimal.Decimal objects.

    Returns:
        A JSON formatted string containing one JSON object.
    """
    for key in d:
        if isinstance(d[key], datetime.datetime):
            d[key] = d[key].isoformat()
        elif isinstance(d[key], Decimal):
            d[key] = float(d[key])

    return json.dumps(d)


def convert_results_to_json_lines(results: list[dict]) -> str:
    """Converts a list of Python dictionaries to a JSON formatted string.

    The JSON object literals in the output string are separated by newlines.

    Args:
        results: A list of dictionaries.

    Returns:
        A string of JSON object literals, delimited by '\n'.
    """
    output = "\n".join([convert_dict_to_json(result) for result in results])
    output += "\n"

    return output
