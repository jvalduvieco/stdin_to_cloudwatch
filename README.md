# cw_metrics_catch
This tool is intended to process output from a system and publish some metrics encoded in the log stream.
It looks for log lines that match a certain format and publishes to Cloudwatch metrics. The lines that not match are not
filtered nor altered and are written to stdout.
The format for the metrics follows:
```json
{
  "Environ/ContentFetchingCron": 
    [
      {
        "ScrapingExecutionTime": 2558219, 
        "Units": "Milliseconds",
      }
    ]
}
```

Possible values for `Units` are:
"Seconds"|"Microseconds"|"Milliseconds"|"Bytes"|"Kilobytes"|"Megabytes"|"Gigabytes"|"Terabytes"|"Bits"|"Kilobits"|"Megabits"|"Gigabits"|"Terabits"|"Percent"|"Count"|"Bytes/Second"|"Kilobytes/Second"|"Megabytes/Second"|"Gigabytes/Second"|"Terabytes/Second"|"Bits/Second"|"Kilobits/Second"|"Megabits/Second"|"Gigabits/Second"|"Terabits/Second"|"Count/Second"|"None"
(Same as [`put-metric-data`](https://docs.aws.amazon.com/cli/latest/reference/cloudwatch/put-metric-data.html) units) 


