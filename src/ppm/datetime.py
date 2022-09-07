from datetime import datetime
import pytz
import time
import os

EPOCH = datetime.utcfromtimestamp(0).replace(tzinfo=pytz.UTC)

# Gives the timestamp (UNIX timestamp) in nanoseconds of the given datetime.
def ns_of_datetime(dt: datetime) -> int:
    return int((dt - EPOCH).total_seconds() * 1000 * 1000 * 1000)


# Convert a ISO string to a datetime
def datetime_from_iso(iso: str) -> datetime:
    dt = datetime.fromisoformat(iso)
    assert dt.tzinfo
    return dt


# tzinfo could be tzinfo.UTC, for instance
def iso_from_datetime(dt: datetime):
    assert dt.tzinfo
    return dt.isoformat()


# Timestamp in nanoseconds, since epoch UNIX (in UTC timezone) to ISO string.
# Returns datetime with tzinfo=tzinfo.UTC
def utc_datetime_from_ns(ns: int) -> datetime:
    return datetime.utcfromtimestamp(ns / (1000 * 1000 * 1000)).replace(tzinfo=pytz.UTC)


# Returns the actual nanoseconds timestamp in the utc timezone
def ns_of_utc_now() -> int:
    return ns_of_datetime(utc_datetime_now())


# Timestamp in nanoseconds, since epoch UNIX (in UTC timezone) to ISO string.
# Returns a ISO similar to this one: '2022-01-17T04:33:40.679826+00:00'
def iso_from_ns(ns: int) -> str:
    return iso_from_datetime(utc_datetime_from_ns(ns))


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
    return datetime.utcnow().replace(tzinfo=pytz.UTC)
