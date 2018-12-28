import os
import sys
import pathlib2

import setuptools
from setuptools.command.install import install

VERSION = "0.0.11"

# The directory containing this file
HERE = pathlib2.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()


class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""
    description = 'verify that the git tag matches our version'

    def run(self):
        tag = os.getenv('CIRCLE_TAG')

        if tag != VERSION:
            info = "Git tag: {0} does not match the version of this app: {1}".format(
                tag, VERSION
            )
            sys.exit(info)


setuptools.setup(
    name="stdin_to_cloudwatch",
    version=VERSION,
    author="Joan Valduvieco",
    author_email="jvalduvieco@gmail.com",
    description="Intercepts json formatted metrics from process stdin and sends to AWS Cloudwatch",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/jvalduvieco/stdin_to_cloudwatch",
    packages=["stdin_to_cloudwatch"],
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    cmdclass={
        'verify': VerifyVersionCommand,
    },
    python_requires='>=2.7',
    install_requires=['boto3'],
    entry_points={"console_scripts": ["stdin_to_cloudwatch=stdin_to_cloudwatch.__main__:main"]},
)
