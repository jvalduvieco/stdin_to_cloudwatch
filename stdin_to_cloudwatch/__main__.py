import sys

import boto3

from stdin_to_cloudwatch.input_adapters import decide_input_adapter
from stdin_to_cloudwatch.output_adapters import stdout_print
from stdin_to_cloudwatch.stream_consumer import eat_stream_and_publish_metrics_until_the_end


def main ():
    client = boto3.client('cloudwatch', region_name=sys.argv[2])
    eat_stream_and_publish_metrics_until_the_end(cw_client=client,
                                                 input_adapter=decide_input_adapter(sys.argv[1]),
                                                 input_stream=sys.stdin,
                                                 instance_id=sys.argv[3] if len(sys.argv) == 4 else None,
                                                 output_function=stdout_print)


if __name__ == "__main__":
    main()
