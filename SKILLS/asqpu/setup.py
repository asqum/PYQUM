import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
if __name__ == '__main__':
    print(setuptools.find_packages(where="asqpu"))
setuptools.setup(
    name="asqpu",
    version="0.0.1",
    author="Hsiao, li-chieh",
    author_email="shiau109@gmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/pypa/sampleproject",
    # project_urls={
    #     "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    # },
    # classifiers=[
    #     "Programming Language :: Python :: 3",
    #     "License :: OSI Approved :: MIT License",
    #     "Operating System :: OS Independent",
    # ],
    install_requires = ['pulse_signal'],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.10",
)

