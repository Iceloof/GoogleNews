import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="GoogleNews",
    version="1.5.1",
    author="Hurin Hu",
    author_email="hurin@live.ca",
    description="Google News search for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Iceloof/GoogleNews",
    packages=setuptools.find_packages(),
    install_requires=['beautifulsoup4','dateparser','python-dateutil'],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
