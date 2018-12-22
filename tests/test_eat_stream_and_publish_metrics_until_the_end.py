from unittest import TestCase
import boto3
from moto import mock_cloudwatch

from cw_metrics_catch import eat_stream_and_publish_metrics_until_the_end, adapt_doing_nothing, adapt_django_logs
import sure  # noqa


class TestEatStreamAndPublishMetricsUntilTheEnd(TestCase):
    @mock_cloudwatch
    def test_eat_stream_and_publish_metrics_until_the_end(self):
        client = boto3.client('cloudwatch', region_name='eu-west-1')
        output = []
        a_stream = ['Error!', '{"EC2/Varnish": [{"Hits": 1, "Type":"Count"}]}', "Warning"]
        eat_stream_and_publish_metrics_until_the_end(input_stream=a_stream,
                                                     cw_client=client, output_function=lambda txt:output.append(txt),
                                                     instance_id=None, input_adapter=adapt_doing_nothing)
        metrics = client.list_metrics()['Metrics']
        metrics.should.have.length_of(1)
        metric = metrics[0]
        metric['Namespace'].should.equal('EC2/Varnish')
        metric['MetricName'].should.equal('Hits')
        output.should.have.length_of(2)
        output[0].should.equal("Error!")
        output[1].should.equal("Warning")

    @mock_cloudwatch
    def test_eat_a_django_logs_stream_and_publish_metrics_until_the_end(self):
        client = boto3.client('cloudwatch', region_name='eu-west-1')
        output = []
        a_stream = ['[22/Dec/2018 00:42:40] ERROR Error!',
                    r"""[22/Dec/2018 00:43:40] INFO {"Environ/ContentFetchingCron": [{"ScrapingExecutionTime": 2558219, "Type": "Milliseconds"}]}""",
                    "[22/Dec/2018 00:44:40] WARN Warning"]
        eat_stream_and_publish_metrics_until_the_end(input_stream=a_stream,
                                                     cw_client=client, output_function=lambda txt:output.append(txt),
                                                     instance_id=None, input_adapter=adapt_django_logs)
        metrics = client.list_metrics()['Metrics']
        metrics.should.have.length_of(1)
        metric = metrics[0]
        metric['Namespace'].should.equal('Environ/ContentFetchingCron')
        metric['MetricName'].should.equal('ScrapingExecutionTime')
        output.should.have.length_of(2)
        output[0].should.equal("[22/Dec/2018 00:42:40] ERROR Error!")
        output[1].should.equal("[22/Dec/2018 00:44:40] WARN Warning")
