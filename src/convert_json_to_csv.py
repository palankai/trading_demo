from contextlib import closing
import argparse
import csv
import json
import os
import statistics
import sys


def main(env, prog, argv):
    args = get_parser(env, prog).parse_args(argv)

    source = json_reader(args.infile)

    records = clean_records(source)

    with_calculated_fields = calculate(records)

    records_with_sma = with_sma(with_calculated_fields, 10)
    records_with_2_smas = with_sma(records_with_sma, 20)

    csv_lines = make_csv_lines(records_with_2_smas)

    writer(csv_lines, args.outfile)

    return 0


def json_reader(infile):
    with closing(infile):
        for line in infile:
            yield json.loads(line)


def clean_records(records):
    for record in records:
        yield dict(
            time=record["time"],
            volume=record["volume"],
            bid=float(record["bid"]["c"]),
            ask=float(record["ask"]["c"]),
        )


def calculate(records):
    for record in records:
        yield dict(
            record,
            mid=(record["ask"] + record["bid"]) / 2,
            spread=round((record["ask"] - record["bid"]) * 100000) / 10
        )


def with_sma(records, n):
    buffer = []
    for record in records:
        buffer = buffer[-n + 1:] + [record["mid"]]
        yield dict(
            record,
            **{f"sma_{n}": len(buffer) == n and statistics.mean(buffer) or "NA"}
        )


def make_csv_lines(records):
    for i, record in enumerate(records):
        if i == 0:
            yield record.keys()
        yield record.values()


def writer(lines, outfile):
    with closing(outfile):
        csv_writer = csv.writer(outfile)
        for line in lines:
            csv_writer.writerow(line)


def get_parser(env, prog):
    parser = argparse.ArgumentParser(prog=prog)
    parser.add_argument(
        "-i", "--infile", nargs="?", type=argparse.FileType("r"), default=sys.stdin
    )
    parser.add_argument(
        "-o", "--outfile", nargs="?", type=argparse.FileType("w"), default=sys.stdout
    )
    return parser


if __name__ == "__main__":
    sys.exit(main(os.environ, sys.argv[0], sys.argv[1:]))
