from setuptools import setup, find_packages

setup(
    name="dltk",
    version="0.1",
    keywords=("pip", "dltk"),
    description="Deeplearning Toolkit",
    long_description="Deeplearning Toolkit",
    license="BSD Licence",
 
    url="https://github.com/bigcat26/dltk",
    author="Chris",
    author_email="bigcat26@gmail.com",
 
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["numpy", "opencv-python", "lmdb", "Pillow"]
)
