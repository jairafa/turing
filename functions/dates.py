import datetime


def convert_str_to_datetime(date_string: str, limit: str):
    """Transformar un string a datetime
    si limit es inicio, le coloca como hora 00:00
    si limit es final, le coloca como hora 23:59
    """
    day: str = ""
    month: str = ""
    year: str = ""
    year, month, day = date_string.split("-")
    # print(f"day {day} month {month} year {year}")
    if limit == "initial":
        return datetime.datetime(
            day=int(day), month=int(month), year=int(year), hour=0, minute=0, second=0
        )
    return datetime.datetime(
        day=int(day), month=int(month), year=int(year), hour=23, minute=59, second=59
    )
