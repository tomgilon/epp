from setuptools import setup, find_packages
setup(
    name="epp",
    version="0.1",
    packages=find_packages(),
    entry_points={
    	'console_scripts': ['epp=epp.main:main']
    },
    install_requires=['virtualenv'],
    include_package_data=True,
)
