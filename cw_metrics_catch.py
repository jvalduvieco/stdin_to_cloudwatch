import json
import sys

import boto3

from cw_metrics_catcher.publish_json_metrics import publish_metrics
import re


def is_json_metric(line):
    return line[0] == '{' and line[-1] == '}'


def adapt_doing_nothing(line):
    return line


def adapt_django_logs(line):
    matches = re.match(r'^\[.+\] \w+ (.+)$', line)
    if matches:
        return matches.groups()[0]
    else:
        return line


def eat_stream_and_publish_metrics_until_the_end(input_stream, output_function, input_adapter, cw_client, instance_id):
    for line in input_stream:
        adapted_line = input_adapter(line)
        if is_json_metric(adapted_line):
            publish_metrics(cw_client, json.loads(adapted_line), instance_id)
        else:
            output_function(line)


def stdout_print(txt):
    print txt


def decide_adapter(adapter_name):
    return adapt_django_logs if adapter_name == 'django' else adapt_doing_nothing


if __name__ == "__main__":
    client = boto3.client('cloudwatch', region_name=sys.argv[2])
    eat_stream_and_publish_metrics_until_the_end(cw_client=client,
                                                 input_adapter=decide_adapter(sys.argv[1]),
                                                 input_stream=sys.stdin,
                                                 instance_id=sys.argv[3] if len(sys.argv) == 4 else None,
                                                 output_function=stdout_print)
