import setuptools
import pathlib2 as pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setuptools.setup(
    name="stdin_to_cloudwatch",
    version="0.0.2",
    author="Joan Valduvieco",
    author_email="jvalduvieco@gmail.com",
    description="Intercepts metrics from stding and sends them to AWS cloudwatch",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/jvalduvieco/stdin_to_cloudwatch",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["boto3", "urllib3"],
    entry_points={"console_scripts": ["stdin_to_cloudwatch=stdin_to_cloudwatch.__main__:main"]},
)
