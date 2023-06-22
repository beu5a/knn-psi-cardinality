from setuptools import setup, find_packages

setup(
    name="fpsica",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'fpsica': ['_psi_ca.so']
    }
)