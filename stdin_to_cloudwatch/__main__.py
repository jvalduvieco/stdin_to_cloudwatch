import sys

import boto3

from stdin_to_cloudwatch.input_adapters import decide_input_adapter
from stdin_to_cloudwatch.output_adapters import stdout_print
from stdin_to_cloudwatch.stream_consumer import eat_stream_and_publish_metrics_until_the_end


def check_arguments():
    if len(sys.argv) < 3:
        print("Wrong number of arguments!")
        print("Usage: stdin_to_cloudwatch <django|none> <region> [instance_id]")
        sys.exit(1)


def main():
    check_arguments()
    input_adapter = sys.argv[1]
    aws_region = sys.argv[2]
    aws_instance_id = sys.argv[3] if len(sys.argv) == 4 else None
    client = boto3.client('cloudwatch', region_name=aws_region)
    eat_stream_and_publish_metrics_until_the_end(cw_client=client,
                                                 input_adapter=decide_input_adapter(input_adapter),
                                                 input_stream=sys.stdin,
                                                 instance_id=aws_instance_id,
                                                 output_function=stdout_print)


if __name__ == "__main__":
    main()
