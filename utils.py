from datetime import datetime


def datetime_from_utc_to_local(utc_str_datetime, format="%H"):  # convert str date to local time
    dt_local = datetime.fromisoformat(utc_str_datetime).astimezone()
    return dt_local.strftime(format), dt_local
