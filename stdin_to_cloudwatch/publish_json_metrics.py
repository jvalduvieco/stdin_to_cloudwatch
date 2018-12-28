def publish_metrics(client, metrics_data, dimensions=None):
    [client.put_metric_data(MetricData=process_namespace_metrics(metrics, dimensions), Namespace=namespace)
     for (namespace, metrics) in metrics_data.items()]


def process_namespace_metrics(metrics, dimensions=None):
    result = []
    catcher_keys = ['Units']
    for metric in metrics:
        if len(metric.keys()) != len(catcher_keys) + 1:
            raise RuntimeError('Wrong object format \'%s\'' % metric)
        key_name = [name for name in metric.keys() if name not in catcher_keys][0]
        result.append(build_one_metric(key_name, metric[key_name], metric['Units'], dimensions))
    return result


def build_one_metric(name, value, unit, dimensions=None):
    result = {
        'MetricName': name,
        'Unit': unit,
        'Value': value
    }
    if dimensions is not None:
        result['Dimensions'] = [
            {
                'Name': name,
                'Value': value
            } for (name, value) in dimensions
        ]
    return result
