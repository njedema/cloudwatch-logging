import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cloudwatch-logging", # Replace with your own username
    version="0.0.2",
    author="Nicolaas Jedema",
    author_email="nj2681@gmail.com",
    url="https://github.com/njedema/cloudwatch-logging/",
    description="A structured JSON logger that seamlessly interoperates with AWS Cloudwatch and other AWS services (e.g. Lambda)",
    keywords=["structured", "logging", "logger", "json", "cloudwatch", "cloud", "watch", "AWS", "aws", "lambda"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.8',
)