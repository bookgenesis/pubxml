from pathlib import Path

from setuptools import find_packages, setup

config = {
    "name": "pubxml",
    "version": "0.0.1",
    "description": "Publishing XML toolkit",
    "url": "https://github.com/bookgenesis/pubxml",
    "author": "Sean Harrison",
    "author_email": "sah@bookgenesis.com",
    "license": "GNU Lesser General Public License v3 (LGPLv3)",
    "classifiers": [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ],
    "entry_points": {},
    "install_requires": [
        "click~=8.1.3",
        "lxml~=4.9.1",
    ],
    "extras_require": {
        "dev": [
            "black~=22.8.0",
            "isort~=5.10.1",
        ],
        "test": [
            "black~=22.8.0",
            "flake8~=5.0.4",
        ],
    },
    "package_data": {"": []},
    "data_files": [],
    "scripts": [],
}

package_path = Path(__file__).absolute().parent
with open(package_path / "README.md", "rb") as f:
    readme = f.read().decode("UTF-8")

setup(
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["contrib", "docs", "tests*"]),
    **config
)
