from datetime import datetime
from utils.utils import MONTHS

current_year = datetime.now().year
YEARS = range(1970, current_year + 1)


def is_date_valid(year=None, month=None, day=None) -> bool:
    try:
        if year is not None:
            try:
                year = int(year)
                if year not in YEARS:
                    raise ValueError
            except ValueError:
                raise ValueError
        if month is not None:
            try:
                month = int(month)
                if month not in range(1, 13):
                    raise ValueError
            except ValueError:
                if month not in MONTHS:
                    raise ValueError
        if day is not None:
            try:
                day = int(day)
                if day not in range(1, 32):
                    raise ValueError
            except ValueError:
                raise ValueError
        return True
    except ValueError:
        return False
