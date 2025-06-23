from setuptools import find_packages, setup

setup(
    name="jaffle_shop_source",
    packages=find_packages(exclude=["jaffle_shop_source_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
