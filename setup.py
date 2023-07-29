from distutils.core import setup
from Cython.Build import cythonize

__version__ = "0.0.1"

extensions = cythonize(
    "src/tabatu/core/tabatu_cpp.pyx",
    language_level="3",
    include_path=["src/tabatu/core"],
)

setup(
    ext_modules=extensions,
    version=__version__,
)
