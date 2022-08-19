from setuptools import setup, find_packages

setup(
    name="emp_burnout",
    version="0.1.0",
    description="End-to-End ML workflow for predicting employee burnout.",
    author="ajkdrag",
    packages=find_packages(include=["emp_burnout", "emp_burnout.*"]),
    install_requires=[
        "Flask==1.1.1",
        "pandas>1.0.0",
        "matplotlib==3.5.1",
        "scikit-learn==1.1.1",
        "xgboost==1.5.0",
        "seaborn==0.11.2",
        "PyYAML==6.0",
        "mlflow==1.28"
    ],
    setup_requires=["flake8"],
)