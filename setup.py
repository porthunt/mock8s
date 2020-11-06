import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mock8s",
    version="0.1.1",
    author="porthunt",
    author_email="porthunt@pm.me",
    description="mock8s is an easy way to test your kubernetes resources.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/porthunt/mock8s",
    packages=setuptools.find_packages(),
    license="Apache",
    install_requires=[
        "decorator",
	"kubernetes",
  	"mock"
    ],
    test_suite="tests",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Apache Software License",
    ],
    python_requires='>=3.6',
)
