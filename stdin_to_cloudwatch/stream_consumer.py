import json

from stdin_to_cloudwatch.publish_json_metrics import publish_metrics


def is_json_metric(line):
    stripped_line = line.strip()
    return stripped_line[0] == '{' and stripped_line[-1] == '}'


def eat_stream_and_publish_metrics_until_the_end(input_stream, output_function, input_adapter, cw_client, dimensions):
    for line in input_stream:
        adapted_line = input_adapter(line)
        if is_json_metric(adapted_line):
            publish_metrics(cw_client, json.loads(adapted_line), dimensions)
        else:
            output_function(line)
