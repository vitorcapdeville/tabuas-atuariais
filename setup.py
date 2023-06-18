from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("src/tabatu_cpp/tabatu_cpp.pyx", language_level="3", include_path=["src/tabatu"])
)
