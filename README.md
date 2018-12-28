# stdin_to_cloudwatch
This tool is intended to process input fromstdin and publish some metrics encoded in the log stream.
It looks for log lines that match a certain format and publishes to Cloudwatch metrics. The lines that not match are neither
filtered nor altered and are written to stdout.
The format for the metrics follows:
```json
{
  "Environ/SomeNamespace": 
    [
      {
        "AMetricName": 2558219, 
        "Units": "Milliseconds",
      }
    ]
}
```

Possible values for `Units` are:
```
"Seconds"|"Microseconds"|"Milliseconds"|"Bytes"|"Kilobytes"|"Megabytes"|"Gigabytes"|"Terabytes"|"Bits"|"Kilobits"|"Megabits"|"Gigabits"|"Terabits"|
"Percent"|"Count"|"Bytes/Second"|"Kilobytes/Second"|"Megabytes/Second"|"Gigabytes/Second"|"Terabytes/Second"|"Bits/Second"|"Kilobits/Second"|"Megabits/Second"|
"Gigabits/Second"|"Terabits/Second"|"Count/Second"|"None"
```

(Same as [`put-metric-data`](https://docs.aws.amazon.com/cli/latest/reference/cloudwatch/put-metric-data.html) units) 

## Usage
```
your_script | stdin_to_cloudwatch -i <django|none> -r <region> [-d <DimensionName=DimensionValue>]
```

Use `stdin_to_cloudwatch -h` for help.

AWS credentials are managed by boto3, so refer to boto [documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#configuration) for further information.

## Intention
Intention behind this tool is to decouple metrics publishing from the main app. With this tool publishing is a responsibility of infrastructure.
