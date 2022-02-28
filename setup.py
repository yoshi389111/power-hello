from setuptools import find_packages, setup

import power_hello.power_hello as power_hello

setup(
    name=power_hello.NAME,
    version=power_hello.VERSION,
    description=power_hello.DESCRIPTION,
    long_description=open("README.rst").read(),
    author=power_hello.AUTHOR,
    author_email=power_hello.AUTHOR_EMAIL,
    url=power_hello.URL,
    license=power_hello.LICENSE,
    py_modules=["power_hello"],
    entry_points={
        "console_scripts": ["power-hello = power_hello.power_hello:main"]},
    packages=find_packages(
        exclude=("docs", "misc")),
)
