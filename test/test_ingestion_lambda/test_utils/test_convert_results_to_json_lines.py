import datetime
from decimal import Decimal
from src.ingestion_lambda.utils.convert_results_to_json_lines import (
    convert_dict_to_json,
    convert_results_to_json_lines,
)


def test_convert_dict_to_json_returns_string():
    assert isinstance(convert_dict_to_json({}), str)


def test_convert_dict_to_json_converts_datetime_to_iso_string():
    assert (
        convert_dict_to_json(
            {"created_at": datetime.datetime(2024, 5, 14, 14, 00, 00, 914000)}
        )
        == '{"created_at": "2024-05-14T14:00:00.914000"}'
    )


def test_convert_dict_to_json_converts_Decimal_to_float():
    assert convert_dict_to_json({"price": Decimal("1.01")}) == '{"price": 1.01}'


def test_convert_results_to_json_lines_returns_string():
    assert isinstance(convert_results_to_json_lines([{"test": 1, "b": "yes"}]), str)


def test_convert_results_to_json_lines_separates_objects_with_newlines():
    input1 = [
        {
            "transaction_id": 11325,
            "transaction_type": "PURCHASE",
            "sales_order_id": None,
            "purchase_order_id": 3349,
            "created_at": datetime.datetime(2024, 4, 25, 13, 0, 9, 818000),
            "last_updated": datetime.datetime(2024, 4, 25, 13, 0, 9, 818000),
        },
        {
            "transaction_id": 11326,
            "transaction_type": "SALE",
            "sales_order_id": 7977,
            "purchase_order_id": None,
            "created_at": datetime.datetime(2024, 4, 25, 13, 40, 10, 219000),
            "last_updated": datetime.datetime(2024, 4, 25, 13, 40, 10, 219000),
        },
    ]

    expected = (
        '{"transaction_id": 11325, "transaction_type": "PURCHASE", "sales_order_id": null, '
        '"purchase_order_id": 3349, "created_at": "2024-04-25T13:00:09.818000", "last_updated": "2024-04-25T13:00:09.818000"}'
        "\n"
        '{"transaction_id": 11326, "transaction_type": "SALE", "sales_order_id": 7977, '
        '"purchase_order_id": null, '
        '"created_at": "2024-04-25T13:40:10.219000", "last_updated": "2024-04-25T13:40:10.219000"}'
        "\n"
    )

    result = convert_results_to_json_lines(input1)

    assert result == expected
