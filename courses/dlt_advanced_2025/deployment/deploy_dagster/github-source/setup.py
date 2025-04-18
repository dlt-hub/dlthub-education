from setuptools import find_packages, setup

setup(
    name="github_source",
    packages=find_packages(exclude=["github_source_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
