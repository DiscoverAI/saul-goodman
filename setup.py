import setuptools

setuptools.setup(
    name="gustavo_fring",
    version="0.1.0",
    author="Daniel Schruhl",
    author_email="danielschruhl@gmail.com",
    description="Pipeline orchestration for drug creation model",
    long_description="Orchestrates all needed steps to create and train a drug creation model.",
    long_description_content_type="text/markdown",
    url="https://github.com/DiscoverAI/gustavo-fring",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
