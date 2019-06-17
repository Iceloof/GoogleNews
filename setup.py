import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="GoogleNews",
    version="1.2.1",
    author="Hurin Hu",
    author_email="hurin@live.ca",
    description="Google News search for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HurinHu/GoogleNews",
    packages=setuptools.find_packages(),
    install_requires=['beautifulsoup4'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
