import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="news_scraper",
    version="0.0.1",
    author="Tomáš Janíček",
    author_email="tomasjanicek221@gmail.com",
    description="Simple scraper for news sites in Slovakia.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TomasJani/news_scraper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)