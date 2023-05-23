from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("src/tabatu/tabatu.pyx", language_level="3", include_path=["src/tabatu"])
)
