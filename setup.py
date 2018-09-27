from setuptools import setup, find_packages

setup(
    name='euclidean',
    version='1.0.0.dev1',
    description='Euclidean geometry library',
    url='https://github.com/keystonetowersystems/euclidean',
    author='Keystone Tower Systems',
    author_email='greg@keystonetowersystems.com',
    packages=find_packages(exclude=('tests',)),
    setup_requires=[
        "tox>=3",
        "coverage>=4"
    ],
    tests_require=[
        "pytest",
        "pytest-cov"
    ],
    install_requires=[
        'numpy>=1.14',
        'matplotlib>=3',
        'sortedcontainers>=2',
        'multipledispatch>=0.6',
        'fuzzyfloat>=1.0.1',
    ],
    zip_safe=False
)
