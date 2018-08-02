from setuptools import setup

setup(
    name="pynteractor",
    version="0.2",
    author="Pierre Wacrenier",
    author_email="pierre@wacrenier.me",
    description="Lib to ease business logic separation",
    url="https://github.com/mota/pynteractor",
    license="ISC",
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "pytest-describe"],
    packages=["pynteractor"],
)
