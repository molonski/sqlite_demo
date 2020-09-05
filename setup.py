import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SQLite_Demo", # Replace with your own username
    version="0.0.1",
    author="Chris Moloney",
    license="GNU GPL",
    description="A small example package for interacting with SQLite Databases.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/molonski/sqlite_demo.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
