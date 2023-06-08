from setuptools import find_packages, setup
from fraud_detection import __version__

setup(
    name='telco_churn',
    packages=find_packages(exclude=['tests', 'tests.*']),
    setup_requires=['wheel'],
    install_requires = ['python-dotenv==0.20.0'],
    version=__version__,
    description='Demo repository implementing an end-to-end MLOps workflow on Databricks. Project derived from dbx '
                'basic python template',
    authors='Rafi Kurlansik, Niall Turbitt, Anastasia Prokaieva'
)
