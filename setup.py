import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().split("\n")

with open("tests/requirements.txt", "r", encoding="utf-8") as fh:
    test_requirements = fh.read().split("\n")

setuptools.setup(
    name="didww_encrypt",
    version="1.0.0",
    author="Denis Talakevich",
    author_email="senid231@gmail.com",
    description="File encryption for DIDWW API 3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/didww/didww_encrypt_python",
    project_urls={
        "Bug Tracker": "https://github.com/didww/didww_encrypt_python/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="DIDWW, encryption",
    packages=["didww_encrypt"],
    python_requires=">=3.6",
    install_requires=requirements,
    test_suite="tests",
    tests_require=test_requirements,
    entry_points={
        "console_scripts": ["didww_encrypt=didww_encrypt.command_line:main"],
    },
    include_package_data=True,
    zip_safe=False,
)
