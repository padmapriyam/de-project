import pandas as pd

# from src.processing_lambda.utils.jsonl_to_df import #get_df_from_s3_bucket


def create_dim_location(df: pd.DataFrame):
    """Updated address to become location.
    Removes created_at and last_updated

    Args:
        dataframe: A pandas dataframe.

    Returns:
        dataframe: A pandas dataframe.

    Raises:
        TypeError if argument is not a pandas dataframe.
        #ValueError if no corresponding department information is #found for any
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError("Argument must be a pandas dataframe")

    location = df.drop(columns=["created_at", "last_updated"])

    location = location.rename(columns={"address_id": "location_id"})

    return location
