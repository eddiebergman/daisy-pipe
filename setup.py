import os
import sys

from setuptools import find_packages, setup

HERE = os.path.abspath(os.path.dirname(__file__))

extras_reqs = {
    "test": [
        "pytest",
        "pytest-cases",
    ],
}


with open(os.path.join(HERE, "README.md")) as fh:
    long_description = fh.read()


setup(
    name="daisy-pipe",
    author="Eddie Bergman",
    author_email="eddiebergmanhs@gmail.com",
    description="Pipes in python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version="0.1.0",
    packages=find_packages(exclude=["test"]),
    extras_require=extras_reqs,
    include_package_data=True,
    license="BSD3",
    platforms=["Linux"],
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Education",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
)
