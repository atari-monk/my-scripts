from setuptools import setup, find_packages

setup(
    name="my-scripts",
    version="0.1",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "info=core.info:main",
            "dsex=core.docs_index.cli:main",
            "ftree=core.file_tree.cli:main",
            "mdex=core.markdown_index.cli:main",
            "taog=core.task_log.cli:main",
            "bome=core.boot_time:main",
        ],
    },
    python_requires=">=3.7",
)