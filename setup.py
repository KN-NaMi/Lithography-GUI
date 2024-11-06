from setuptools import setup, find_packages

setup(
    name="Lithography-GUI",
    version="0.1.0",
    packages=find_packages(),  
    install_requires=[
        "serial==0.0.97",
        "nicegui==2.4",
        "setuptools==75.2.0",
        "pywebview==5.3.2"
    ],
    python_requires=">=3.12.1",

)
