import pandas as pd

try:
    from utils.jsonl_to_df import get_df_from_s3_bucket
except ModuleNotFoundError:
    from src.processing_lambda.utils.jsonl_to_df import get_df_from_s3_bucket


def create_dim_counterparty(df: pd.DataFrame):
    """Adds full address details to dataframe and returns
    a new dataframe with these columns.

    This function uses legal_address_id to get the specific address details
    from the address table data.

    This function returns a new dataframe as we were limited by the
    functionality of the pandas dataframe merge method.

    Args:
        dataframe: A pandas dataframe.

    Returns:
        dataframe: A pandas dataframe.

    Raises:
        TypeError if argument is not a pandas dataframe.
        ValueError if no corresponding address information is found for any
        of the address ids in the counterparty dataframe.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Argument must be a pandas dataframe")

    address_df = get_df_from_s3_bucket("address")

    new_df = df.merge(
        address_df, how="left", left_on="legal_address_id", right_on="address_id"
    )

    if (
        any(pd.isna(new_df["address_line_1"]))
        or any(pd.isna(new_df["city"]))
        or any(pd.isna(new_df["postal_code"]))
        or any(pd.isna(new_df["country"]))
        or any(pd.isna(new_df["phone"]))
    ):
        raise ValueError("One or more of the address fields are empty.")

    new_df.rename(
        columns={
            "address_line_1": "counterparty_legal_address_line_1",
            "address_line_2": "counterparty_legal_address_line_2",
            "city": "counterparty_legal_city",
            "district": "counterparty_legal_district",
            "postal_code": "counterparty_legal_postal_code",
            "country": "counterparty_legal_country",
            "phone": "counterparty_legal_phone_number",
        },
        inplace=True,
    )

    return new_df[
        [
            "counterparty_id",
            "counterparty_legal_name",
            "counterparty_legal_address_line_1",
            "counterparty_legal_address_line_2",
            "counterparty_legal_district",
            "counterparty_legal_city",
            "counterparty_legal_postal_code",
            "counterparty_legal_country",
            "counterparty_legal_phone_number",
        ]
    ]
