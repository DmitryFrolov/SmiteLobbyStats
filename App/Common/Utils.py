import os
import hashlib
import datetime
import json


def generate_md5(dev_id, method_name, auth_key, utc_timestamp):
    target = dev_id + method_name + auth_key + utc_timestamp
    return hashlib.md5(target.encode('utf-8')).hexdigest()


def make_date():
    tt = datetime.datetime.utcnow().utctimetuple()
    result_date = ""
    for chunk in [tt.tm_year, tt.tm_mon, tt.tm_mday]:
        result_date += str(chunk).zfill(2)
    return result_date


def make_timestamp():
    tt = datetime.datetime.utcnow().utctimetuple()
    result_timestamp = ""
    for chunk in [tt.tm_year, tt.tm_mon, tt.tm_mday, tt.tm_hour, tt.tm_min, tt.tm_sec]:
        result_timestamp += str(chunk).zfill(2)
    return result_timestamp


def get_last_10m_frame():
    tt = datetime.datetime.utcnow().utctimetuple()
    result_timestamp = ""
    for chunk in [tt.tm_hour, tt.tm_min]:
        result_timestamp += str(chunk).zfill(2)
    return result_timestamp


def json_contents(fpath: str) -> dict:
    try:
        with open(fpath, 'r') as f:
            return json.load(f)
    except:
        raise RuntimeError(f'Missing file: {os.path.abspath(fpath)}')


def dump_to_json(fpath: str, data: dict) -> None:
    os.makedirs(os.path.dirname(fpath), exist_ok=True)
    with open(fpath, 'w+') as outfile:
        json.dump(data, outfile)
