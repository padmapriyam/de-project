import pandas as pd
from pandas import DatetimeIndex
from datetime import datetime, date


def create_dim_date(dates):
    """Adds specified columns from dataframe and returns dataframe.

    This function is used to add dates to the date dimension table using timestamp and return the dataframe.

    This function intentionally mutates the input dataframe as we do not wish to replicate the data in memory and we will not need the old dataframe again.

    Args:
        date: A list of datetime.data objects.

    Returns:
        dataframe: A pandas dataframe.

    Raises:
        TypeError if arguments do not conform to expected types.
    """

    if not isinstance(dates, list):
        raise TypeError("Input needs to be a list of datetime.date objects!")

    if not all(isinstance(d, date) for d in dates):
        raise TypeError(
            "All elements in the list need to be a list of datetime.date objects!"
        )

    dim_date = pd.DataFrame(
        {
            "date_id": dates,
            "year": [date.year for date in dates],
            "month": [date.month for date in dates],
            "day": [date.day for date in dates],
            "day_of_week": [date.weekday() for date in dates],
            "day_name": [date.strftime("%A") for date in dates],
            "month_name": [date.strftime("%B") for date in dates],
            "quarter": [(date.month - 1) // 3 + 1 for date in dates],
        }
    )

    return dim_date
