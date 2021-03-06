from setuptools import setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="src",
    version="0.0.1",
    author="Bappy Ahmed",
    description="A small package for Activity Recognition system based on Multisensor data fusion (AReM) Data Set",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/entbappy/Activity_Recognition_UCI",
    author_email="entbappy73@gmail.com",
    packages=["src"],
    python_requires=">=3.7",
    install_requires=[
        'dvc',
        'pandas',
        'scikit-learn',
        'pandas-profiling',
        'numpy',
        'joblib',
        'PyYAML'
    ]
)