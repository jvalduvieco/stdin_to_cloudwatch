import json
import sys

import boto3

from cw_metrics_catcher.publish_json_metrics import publish_metrics


def is_json_metric(line):
    return line[0] == '{' and line[-1] == '}'


def eat_stream_and_publish_metrics_until_the_end(input_stream, cw_client, output_function, instance_id):
    for line in input_stream:
        if is_json_metric(line):
            publish_metrics(cw_client, json.loads(line), instance_id)
        else:
            output_function(line)


def stdout_print(txt):
    print txt


if __name__ == "__main__":
    client = boto3.client('cloudwatch', region_name=sys.argv[1])
    eat_stream_and_publish_metrics_until_the_end(input_stream=sys.stdin,
                                                 cw_client=client,
                                                 output_function=stdout_print,
                                                 instance_id=sys.argv[2] if len(sys.argv) == 3 else None)
