import pandas as pd


def convert_dataframe_to_parquet(dataframe: pd.DataFrame):
    """Takes a dataframe and returns its data in parquet format.

    Args:
        dataframe: A pandas dataframe.

    Returns:
        bytes of binary parquet format

    Raises:
        TypeError if argument is not a pandas dataframe.
        ValueError if dataframe is empty.
    """
    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError("Argument must be a pandas DataFrame")

    if dataframe.empty:
        raise ValueError("Attempted to convert empty dataframe to parquet")

    parquet_data = dataframe.to_parquet()

    return parquet_data
