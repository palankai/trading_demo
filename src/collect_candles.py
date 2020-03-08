import argparse
import sys
import os
import pprint
import json

import requests


def main(env, prog, argv):
    base_url = env.get("API_ENDPOINT")
    access_token = env.get("ACCESS_TOKEN")
    if not base_url or not access_token:
        print("API_ENDPOINT and ACCESS_TOKEN environment variables are required")
        return 1
    args = get_parser(env, prog).parse_args(argv)
    data_path = args.datapath

    print(f"Collecting {args.instrument}...")
    start_time = "2017-01-01T00:00:00.00Z"
    end_time = "2020-02-18T00:00:00.00Z"
    granularity = args.granularity
    instrument = args.instrument

    with open(os.path.join(data_path, f"{instrument}_{granularity}.txt"), "w") as fh:
        for candle in fetch_all(
            base_url=base_url,
            access_token=access_token,
            instrument=instrument,
            granularity=granularity,
            start_time=start_time,
            end_time=end_time
        ):
            print(candle["time"])
            fh.write(json.dumps(candle))
            fh.write("\n")


def get_parser(env, prog):
    parser = argparse.ArgumentParser(prog=prog)
    parser.add_argument("instrument", type=str)
    parser.add_argument("granularity", type=str)
    parser.add_argument("datapath", type=str)
    return parser


def fetch_all(*, base_url, access_token, instrument, granularity, start_time, end_time):
    include_first = True
    while True:
        page = fetch_page(
            base_url=base_url,
            access_token=access_token,
            instrument=instrument,
            granularity=granularity,
            start_time=start_time,
            include_first=include_first
        )
        for candle in page["candles"]:
            if candle["time"] < end_time:
                yield candle
            else:
                return
        if page["candles"][-1]["time"] < end_time:
            start_time = page["candles"][-1]["time"]
            include_first = False


def fetch_page(
    *, base_url, access_token, instrument, granularity, start_time, include_first
):
    url = f"{base_url}/v3/instruments/{instrument}/candles"
    headers = {
        "Authorization": f"bearer {access_token}",
        "Content-Type": "application/json"
    }
    params = {
        "price": "BA",
        "granularity": granularity,
        "from": start_time,
        "count": 5000,
        "includeFirst": include_first
    }
    response = requests.get(url, headers=headers, params=params)
    assert response.status_code == 200, f"{response.status_code}, {response.text}"
    return response.json()


if __name__ == "__main__":
    sys.exit(main(os.environ, sys.argv[0], sys.argv[1:]))
