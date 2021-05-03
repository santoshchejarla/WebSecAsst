from setuptools import setup, find_packages

setup(
    name="WebSecAsst",
    version='1.0.1',
    desription="WebSec Asst",
    packages=['WebSecAsst'],
    install_requires=[
        "requests",
        "tldextract",
        "whois",
        "urllib3",
        "pyOpenSSL",
        "scikit-learn",
        "beautifulsoup4",
        "pickle-mixin",
        "xgboost",
        "numpy",
        "pandas"
    ]
)