import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="didww-encrypt",  # Replace with your own username
    version="1.0.0",
    author="Denis Talakevich",
    author_email="senid231@gmail.com",
    description="File encryption for DIDWW API 3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/didww/didww-encrypt-sdk-python",
    project_urls={
        "Bug Tracker": "https://github.com/didww/didww-encrypt-sdk-python/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="",
    packages=["didww_encrypt"],
    python_requires=">=3.6",
    install_requires=[
        "pycryptodomex",
    ],
    test_suite="nose.collector",
    tests_require=["nose", "nose-cover3"],
    entry_points={
        "console_scripts": ["didww_encrypt=didww_encrypt.command_line:main"],
    },
    include_package_data=True,
    zip_safe=False
)
