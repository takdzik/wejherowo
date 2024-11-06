from setuptools import setup, find_packages

setup(
    name="wejherowo",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    entry_points={
        'console_scripts': [
            'wejherowo=wejherowo.cli:main',
        ],
    },
)