from setuptools import setup, find_packages

setup(
    name="my-scripts",
    version="0.1",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "mdindex=core.markdown_indexer.cli:main",
        ],
    },
    python_requires=">=3.7",
)