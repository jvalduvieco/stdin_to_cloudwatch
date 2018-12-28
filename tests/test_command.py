import os
from unittest import TestCase

from moto import mock_cloudwatch
from stdin_to_cloudwatch.__main__ import main
import sure  # noqa


class TestEatStreamAndPublishMetricsUntilTheEnd(TestCase):
    @mock_cloudwatch
    def test_parses_arguments_and_eats_stream_and_publish_metrics_until_the_end(self):
        fake_stdin = ['[22/Dec/2018 00:42:40] ERROR Error!',
                      r"""[22/Dec/2018 00:43:40] INFO {"Environ/ContentFetchingCron": [{"ScrapingExecutionTime": 2558219, "Units": "Milliseconds"}]}""",
                      "[22/Dec/2018 00:44:40] WARN Warning"]
        output = []
        result = main(fake_stdin,
                      ["--input_adapter", "django", "--region", "eu-west-1", "--dimensions", "EnvironmentName=prod"],
                      lambda txt: output.append(txt))
        output.should.have.length_of(2)
        output[0].should.equal("[22/Dec/2018 00:42:40] ERROR Error!")
        output[1].should.equal("[22/Dec/2018 00:44:40] WARN Warning")
        result.should.equal(os.EX_OK)

    @mock_cloudwatch
    def test_parses_short_arguments_and_eats_stream_and_publish_metrics_until_the_end(self):
        fake_stdin = ['[22/Dec/2018 00:42:40] ERROR Error!',
                      r"""[22/Dec/2018 00:43:40] INFO {"Environ/ContentFetchingCron": [{"ScrapingExecutionTime": 2558219, "Units": "Milliseconds"}]}""",
                      "[22/Dec/2018 00:44:40] WARN Warning"]
        output = []
        result = main(fake_stdin, ["--i", "django", "-r", "eu-west-1", "-d", "EnvironmentName=prod"],
                      lambda txt: output.append(txt))
        output.should.have.length_of(2)
        output[0].should.equal("[22/Dec/2018 00:42:40] ERROR Error!")
        output[1].should.equal("[22/Dec/2018 00:44:40] WARN Warning")
        result.should.equal(os.EX_OK)
