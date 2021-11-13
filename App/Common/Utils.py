import os
import hashlib
import datetime
import json


def generate_md5(dev_id, method_name, auth_key, utc_timestamp):
    target = dev_id + method_name + auth_key + utc_timestamp
    return hashlib.md5(target.encode('utf-8')).hexdigest()


def current_utc_time():
    return datetime.datetime.utcnow()


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
