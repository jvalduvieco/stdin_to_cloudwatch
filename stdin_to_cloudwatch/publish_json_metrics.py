def publish_metrics(client, metrics_data, instance_id=None):
    [client.put_metric_data(MetricData=process_namespace_metrics(metrics, instance_id), Namespace=namespace)
     for (namespace, metrics) in metrics_data.items()]


def process_namespace_metrics(metrics, instance_id=None):
    result = []
    catcher_keys = ['Units']
    for metric in metrics:
        if len(metric.keys()) != len(catcher_keys) + 1:
            raise RuntimeError('Wrong object format \'%s\'' % metric)
        key_name = [name for name in metric.keys() if name not in catcher_keys][0]
        result.append(build_one_metric(key_name, metric[key_name], metric['Units'], instance_id))
    return result


def build_one_metric(name, value, unit, instance_id=None):
    result = {
        'MetricName': name,
        'Unit': unit,
        'Value': value
    }
    if instance_id is not None:
        result['Dimensions'] = [
            {
                'Name': 'InstanceId',
                'Value': instance_id
            },
        ]
    return result
