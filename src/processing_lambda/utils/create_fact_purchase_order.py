import pandas as pd

try:
    from utils.create_dim_date import create_dim_date
except ModuleNotFoundError:
    from src.processing_lambda.utils.create_dim_date import create_dim_date


def create_fact_purchase_order(df: pd.DataFrame):
    """Transforms an incoming dataframe comprising information from the payment
    table into the schema required for the fact_purchase_order table.

    Returns dataframes for fact_purchase_order table and dim_date table.

    This function mutates the input dataframe.

    Args:
        df: A pandas dataframe.

    Returns:
        A tuple containing two pandas dataframes:
        Dataframe for fact_purchase_order.
        Dataframe for dim_date.

    Raises:
        TypeError when the argument is not a pandas dataframe.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Argument must be a pandas dataframe")

    # Convert varchar dates to datetime.date
    df["agreed_delivery_date"] = pd.to_datetime(df["agreed_delivery_date"]).dt.date
    df["agreed_payment_date"] = pd.to_datetime(df["agreed_payment_date"]).dt.date

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
                "purchase_order_id",
                "created_date",
                "created_time",
                "last_updated_date",
                "last_updated_time",
                "staff_id",
                "counterparty_id",
                "item_code",
                "item_quantity",
                "item_unit_price",
                "currency_id",
                "agreed_delivery_date",
                "agreed_payment_date",
                "agreed_delivery_location_id",
            ]
        ],
        dim_date_df,
    )
