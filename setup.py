import setuptools

with open("README.md", "r") as fh:

    long_description = fh.read()

setuptools.setup(

    name="ServerAPI",

    version="1.0.0",

    author="HenryGJackson",

    description="Framework to create a remote API",

    long_description=long_description,

    long_description_content_type="text/markdown",

    url="https://github.com/HenryGJackson/Server-API",

    packages=['ServerAPI'],

    classifiers=[

        "Programming Language :: Python :: 3",

        "License :: None",

        "Operating System :: OS Independent",
    ],

    python_requires='>=3.6',

)