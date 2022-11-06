from datetime import datetime, timezone
from typing import Union, Tuple
from decimal import Decimal
import time
import os

EPOCH = datetime.utcfromtimestamp(0).replace(tzinfo=timezone.utc)

# Gives the timestamp (UNIX timestamp) in nanoseconds of the given datetime.
def ns_of_datetime(dt: datetime) -> int:
    return int((dt - EPOCH).total_seconds() * 1000 * 1000 * 1000)


# Convert a ISO string to a datetime
def datetime_from_iso(iso: str) -> datetime:

    # https://discuss.python.org/t/parse-z-timezone-suffix-in-datetime/2220/9
    iso = iso.replace('Z', '+00:00')
    
    dt = datetime.fromisoformat(iso)
    assert dt.tzinfo
    return dt


# tzinfo could be tzinfo.UTC, for instance
def iso_from_datetime(dt: datetime):
    assert dt.tzinfo
    return dt.isoformat()


# Timestamp in nanoseconds, since epoch UNIX (in UTC timezone) to ISO string.
# Returns datetime with tzinfo=tzinfo.UTC
def utc_datetime_from_ns(ns: Union[int, float, Decimal]) -> datetime:
    return datetime.utcfromtimestamp(float(ns / (1000 * 1000 * 1000))).replace(tzinfo=timezone.utc)


# Returns the actual nanoseconds timestamp in the utc timezone
def ns_of_utc_now() -> int:
    return ns_of_datetime(utc_datetime_now())


# Timestamp in nanoseconds, since epoch UNIX (in UTC timezone) to ISO string.
# Returns a ISO similar to this one: '2022-01-17T04:33:40.679826+00:00'
def iso_from_ns(ns: Union[int, float, Decimal]) -> str:
    return iso_from_datetime(utc_datetime_from_ns(ns))


# Get datetime from timestamp in nanoseconds since EPOCH. It returns datetime in UTC timezone.
def datetime_from_ns(ns: Union[int, float, Decimal]) -> datetime:
    return datetime.utcfromtimestamp(float(ns / (1000 * 1000 * 1000))).replace(tzinfo=timezone.utc)


# Get somethine like '+05:00', that represents the current timezone of the current device.
def get_my_iso_timezone() -> str:
    return str.format('{0:+06.2f}', float(time.timezone) / 3600).replace('.', ':')


# UTC timestamp (UNIX timestamp) in nanoseconds of the creation of a file
def ns_of_file_creation(filepath: str) -> int:
    seg = os.path.getctime(filepath) - time.timezone
    return int(seg * 1000 * 1000 * 1000)


# Returns datetime with tzinfo=tzinfo.UTC of the time of the creation of the file
def utc_datetime_of_file_creation(filepath: str) -> datetime:
    return utc_datetime_from_ns(ns_of_file_creation(filepath))


# Return now datetime with tzinfo = UTC
def utc_datetime_now() -> datetime:
    return datetime.utcnow().replace(tzinfo=timezone.utc)


# Extract the date and hour. Example: '2022-01-08' and '16:50:51.105836'
def date_and_hour_from_ns(ns: int) -> Tuple[str, str]:
    iso = iso_from_ns(ns)
    day_str: str =   iso[0:10] 
    hour_str: str = iso[11:-6]
    return day_str, hour_str
