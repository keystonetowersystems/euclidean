from setuptools import setup, find_packages

INSTALL_REQUIRES = ["sortedcontainers>=2", "multipledispatch>=0.6"]
EXTRAS_REQUIRE = {
    "docs": [],
    "tests": ["pytest", "coverage"],
    "siquant": ["siquant==4.0.0b5"],
}

setup(
    name="euclidean",
    version="1.0.0b1",
    description="Euclidean Geometry Library",
    url="https://github.com/keystonetowersystems/euclidean",
    author="Keystone Tower Systems",
    author_email="greg@keystonetowersystems.com",
    packages=find_packages(exclude=("tests",)),
    setup_requires=["tox>=3"],
    extras_require=EXTRAS_REQUIRE,
    install_requires=INSTALL_REQUIRES,
    zip_safe=False,
)
