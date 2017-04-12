from setuptools import setup

setup(
    name="pynteractor",
    version="0.1",
    author="Pierre Wacrenier",
    author_email="mota@souitom.org",
    description="Lib to ease business logic separation",
    url="http://github.com/mota/pynteractor",
    license="ISC",
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "pytest-describe"],
    packages=["pynteractor"],
)
