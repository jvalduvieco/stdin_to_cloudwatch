import os
import sys
import argparse

import boto3

from stdin_to_cloudwatch.input_adapters import decide_input_adapter
from stdin_to_cloudwatch.output_adapters import stdout_print
from stdin_to_cloudwatch.stream_consumer import eat_stream_and_publish_metrics_until_the_end


def main(input_stream, args, stdout_callback):
    try:
        args = parse_arguments(args)

        client = boto3.client('cloudwatch', region_name=args.region)
        eat_stream_and_publish_metrics_until_the_end(cw_client=client,
                                                     input_adapter=decide_input_adapter(args.input_adapter),
                                                     input_stream=input_stream,
                                                     dimensions=build_dimensions_array(args),
                                                     output_function=stdout_callback)
        return os.EX_OK
    except Exception as e:
        print (e)
        return os.EX_SOFTWARE


def parse_arguments(args):
    parser = argparse.ArgumentParser(
        description='Ingest stdin, publish metrics to cloudwatch, pass through the rest.')
    parser.add_argument('-d', '--dimensions', nargs='+', default=[])
    parser.add_argument('-r', '--region', nargs='?', help='desired AWS Cloudwatch region ', required=True)
    parser.add_argument('-i', '--input_adapter', choices=['none', 'django'], nargs='?', required=True,
                        help='function applied to all input lines to remove timestamps, levels, ...')
    args = parser.parse_args(args)
    return args


def build_dimensions_array(args):
    return [tuple(s.split('=')) for s in args.dimensions]


if __name__ == "__main__":
    sys.exit(main(sys.stdin, sys.argv[1:], stdout_print))
