from Common.Utils import current_utc_time

def make_timestamp(time=current_utc_time()):
    # return a string with current year, month, day, hour, min and sec as zero-padded decimals (ex. 20210101110112)
    return time.strftime("%Y%m%d%H%M%S")

def make_date(time=current_utc_time()):
    # return a string with current year, month and day as zero-padded decimals (ex. 20210101, 20201212)
    return time.strftime("%Y%m%d")

def get_hour(time=current_utc_time()):
    # return a string with current hour as zero-padded decimal
    return time.strftime("%H")
