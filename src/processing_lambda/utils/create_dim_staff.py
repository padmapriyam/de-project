import pandas as pd

try:
    from utils.jsonl_to_df import get_df_from_s3_bucket
except ModuleNotFoundError:
    from src.processing_lambda.utils.jsonl_to_df import get_df_from_s3_bucket


def create_dim_staff(df: pd.DataFrame):
    """Adds department_name and location columns to dataframe and returns
    a new dataframe with these columns.

    This function uses department_id to get the department_name and location
    from the department table data.

    This function returns a new dataframe as we were limited by the
    functionality of the pandas dataframe merge method.

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

    department_df = get_df_from_s3_bucket("department")

    new_df = df.merge(department_df, how="left", on="department_id")

    if any(pd.isna(new_df["department_name"])):
        raise ValueError("department_name or location not found")

    return new_df[
        [
            "staff_id",
            "first_name",
            "last_name",
            "department_name",
            "location",
            "email_address",
        ]
    ]
