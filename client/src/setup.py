from setuptools import setup, find_packages

setuptools.setup(
    name='gochat',
    version='1.0.1',
    install_requires=['pymongo==3.3.0', 'requests==2.31.0', 'pyfiglet==0.7.5'],
    packages=find_packages(),
    url='https://github.com/abhijith0505/GoChat',
    entry_points={
        'console_scripts': [
            'gochat = gochat:main'
        ]
    },
    include_package_data = True
)
