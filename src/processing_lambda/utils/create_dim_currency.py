import pandas as pd


def create_dim_currency(df: pd.DataFrame):
    """Adds specified columns from dataframe and returns dataframe.

    This function is used to add currency name corresponding to the currency code and return the dataframe.

    This function intentionally mutates the input dataframe as we do not wish to replicate the data in memory and we will not need the old dataframe again.

    Args:
        dataframe: A pandas dataframe.

    Returns:
        dataframe: A pandas dataframe.

    Raises:
        TypeError if arguments do not conform to expected types.
        KeyError if the currency code is not present in the currency name dict
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input needs to be of type dataframe!")
    currency_name = {
        "GBP": "Pound Sterling",
        "USD": "United States Dollar",
        "EUR": "Euro",
    }
    try:
        df["currency_name"] = df.apply(
            lambda row: currency_name[row.currency_code], axis=1
        )
        return df[["currency_id", "currency_code", "currency_name"]]
    except KeyError as e:
        raise KeyError(f"Currency code {e} not found!!")
