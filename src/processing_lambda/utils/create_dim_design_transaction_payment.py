import pandas as pd


def drop_update_created_at_two_columns(df: pd.DataFrame):
    """

    This function drops "last_updated", "created_at" columns.
    The input dataframe is mutatated in this function.

    Args:
        dataframe: A pandas dataframe.

    Returns:
        dataframe: A pandas dataframe.

    Raises:
        TypeError if argument is not a pandas dataframe.
        ValueError if no corresponding department information is found for any
        of the department ids in the staff dataframe.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Argument must be a pandas dataframe")

    df.drop(columns=["last_updated", "created_at"], inplace=True)

    return df
