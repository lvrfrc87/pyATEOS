import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyateos",
    version="0.1.6",
    author="Federico Olivieri",
    author_email="lvrfrc87@gmail.com",
    description="python framework to test operational status of an Arista network",
    scripts=['pyateos/pyateos'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/networkAutomation/pyateos",
    packages=setuptools.find_packages(),
    install_requires=[
        'jsondiff>=1.2.0',
        'pyeapi>=0.8.3',
        'jmespath>=0.9.5',
        ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)