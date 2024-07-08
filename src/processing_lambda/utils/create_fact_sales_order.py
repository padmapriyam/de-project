import pandas as pd

try:
    from utils.create_dim_date import create_dim_date
except ModuleNotFoundError:
    from src.processing_lambda.utils.create_dim_date import create_dim_date


def create_fact_sales_order(df: pd.DataFrame):
    """Transforms an incoming dataframe comprising information from the sales
    table into the schema required for the fact_sales_order table.

    Returns dataframes for fact_sales_order table and dim_date table.

    This function mutates the input dataframe.

    Args:
        df: A pandas dataframe.

    Returns:
        A tuple containing two pandas dataframes:
        Dataframe for fact_sales_order.
        Dataframe for dim_date.

    Raises:
        TypeError when the argument is not a pandas dataframe.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Argument must be a pandas dataframe")

    df.rename(columns={"staff_id": "sales_staff_id"}, inplace=True)

    # Convert varchar dates to datetime.date
    for agreed_date in ("agreed_delivery_date", "agreed_payment_date"):
        df[agreed_date] = pd.to_datetime(df[agreed_date]).dt.date

    created_datetime = pd.to_datetime(df["created_at"], format="mixed")
    df["created_date"] = created_datetime.dt.date
    df["created_time"] = created_datetime.dt.time

    updated_datetime = pd.to_datetime(df["last_updated"], format="mixed")
    df["last_updated_date"] = updated_datetime.dt.date
    df["last_updated_time"] = updated_datetime.dt.time

    # find unique dates in dataframe
    date_series = pd.concat(
        [
            df["created_date"],
            df["last_updated_date"],
            df["agreed_delivery_date"],
            df["agreed_payment_date"],
        ]
    ).unique()

    # pass these dates as a list to the create_dim_date function
    dim_date_df = create_dim_date(list(date_series))

    return (
        df[
            [
                "sales_order_id",
                "created_date",
                "created_time",
                "last_updated_date",
                "last_updated_time",
                "sales_staff_id",
                "counterparty_id",
                "units_sold",
                "unit_price",
                "currency_id",
                "design_id",
                "agreed_payment_date",
                "agreed_delivery_date",
                "agreed_delivery_location_id",
            ]
        ],
        dim_date_df,
    )
