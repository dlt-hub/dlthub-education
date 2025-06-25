from setuptools import find_packages, setup

setup(
    name="parallel_pipeline",
    packages=find_packages(exclude=["parallel_pipeline_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
