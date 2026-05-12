from setuptools import setup, find_packages

setup(
    name="api-tracker",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Django>=3.2",
        "djangorestframework"
    ],
    description="API tracking system",
    author="Pulkit",
)