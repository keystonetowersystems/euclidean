from setuptools import setup, find_packages

setup(
    name='euclidean',
    version='0.1.1',
    description='2d euclidean geometry library',
    url='https://github.com/keystonetowersystems/euclidean',
    author='Keystone Tower Systems',
    author_email='greg@keystonetowersystems.com',
    packages=find_packages(exclude=('tests',)),
    install_requires=[
        'sortedcontainers>=2',
        'multipledispatch>=0.6',
        'fuzzyfloat>=1.0.0.dev1'
    ],
    zip_safe=False
)
