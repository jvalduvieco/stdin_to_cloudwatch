from unittest import TestCase

from stdin_to_cloudwatch.publish_json_metrics import process_namespace_metrics
import sure  # noqa


class TestProcessNamespaceMetrics(TestCase):
    def test_should_create_a_metric_from_a_dict(self):
        result = process_namespace_metrics([{'Hits': 33, 'Units': 'Count'}])
        metric = result[0]
        metric['MetricName'].should.equal('Hits')
        metric['Value'].should.equal(33)
        metric['Unit'].should.equal('Count')

    def test_should_add_a_dimension_to_a_metric_if_provided(self):
        result = process_namespace_metrics([{'Hits': 33, 'Units': 'Count'}], [('InstanceId', 'i-223455')])
        metric = result[0]
        metric['MetricName'].should.equal('Hits')
        metric['Value'].should.equal(33)
        metric['Unit'].should.equal('Count')
        metric['Dimensions'][0]['Name'].should.equal('InstanceId')
        metric['Dimensions'][0]['Value'].should.equal('i-223455')

    def test_should_add_multiple_dimension_to_a_metric_if_provided(self):
        result = process_namespace_metrics([{'Hits': 33, 'Units': 'Count'}],
                                           [('InstanceId', 'i-223455'), ('EnvironmentId', 'prod')])
        metric = result[0]
        metric['MetricName'].should.equal('Hits')
        metric['Value'].should.equal(33)
        metric['Unit'].should.equal('Count')
        metric['Dimensions'].should.have.length_of(2)
        metric['Dimensions'][0]['Name'].should.equal('InstanceId')
        metric['Dimensions'][0]['Value'].should.equal('i-223455')
        metric['Dimensions'][1]['Name'].should.equal('EnvironmentId')
        metric['Dimensions'][1]['Value'].should.equal('prod')

    def test_throws_an_exception_on_bad_formatted_object(self):
        with self.assertRaises(RuntimeError):
            self.assertRegexpMatches = 'This is broken'
            process_namespace_metrics([{'Hits': 33, 'Units': 'Count', 'IShouldNotBeHere': 1}])
