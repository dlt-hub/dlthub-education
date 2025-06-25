from setuptools import find_packages, setup

setup(
    name="dlt_dagster_integration_sequential_pipeline",
    packages=find_packages(exclude=["dlt_dagster_integration_sequential_pipeline_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
