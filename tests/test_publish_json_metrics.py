import json
from unittest import TestCase

import boto3
from moto import mock_cloudwatch
from stdin_to_cloudwatch.publish_json_metrics import publish_metrics
import sure  # noqa


class TestPublishJsonMetrics(TestCase):
    @mock_cloudwatch
    def test_should_publish_a_metric_from_json(self):
        client = boto3.client('cloudwatch', 'eu-west-1')
        publish_metrics(client, json.loads('{"EC2/Varnish": ['
                                           '{"Hits": 1, "Units":"Count"}, '
                                           '{"Misses": 2, "Units":"Count"}, '
                                           '{"Uptime": 230, "Units":"Seconds"}'
                                           ']}'))
        metrics = client.list_metrics()['Metrics']
        metrics.should.have.length_of(3)
        metric = metrics[0]
        metric['Namespace'].should.equal('EC2/Varnish')
        metric['MetricName'].should.equal('Hits')

    @mock_cloudwatch
    def test_should_publish_several_metrics_from_json(self):
        client = boto3.client('cloudwatch', 'eu-west-1')
        publish_metrics(client, json.loads('{"EC2/Varnish": ['
                                           '{"Hits": 1, "Units":"Count"}, '
                                           '{"Misses": 2, "Units":"Count"}, '
                                           '{"Uptime": 230, "Units":"Seconds"}'
                                           ']}'))
        metrics = client.list_metrics()['Metrics']
        metrics.should.have.length_of(3)
        metric = metrics[0]
        metric['Namespace'].should.equal('EC2/Varnish')
        metric['MetricName'].should.equal('Hits')
        metric = metrics[1]
        metric['Namespace'].should.equal('EC2/Varnish')
        metric['MetricName'].should.equal('Misses')
        metric = metrics[2]
        metric['Namespace'].should.equal('EC2/Varnish')
        metric['MetricName'].should.equal('Uptime')
