import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyateos",
    version="1.0.0",
    author="Federico Olivieri",
    author_email="lvrfrc87@gmail.com",
    description="python framework for operational status test on Arista network",
    scripts=['pyateos/pyateos'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/networkAutomation/pyateos",
    packages=setuptools.find_packages(),
    install_requires=['jsondiff>=1.2.0','pyeapi>=0.8.3'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)