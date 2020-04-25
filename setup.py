from setuptools import setup
from unasync import build_py

setup(
    name="sleepy",
    version="0",
    license="CC0-1.0",
    packages=["sleepy", "sleepy._async", "sleepy.backends",],
    cmdclass={"build_py": build_py},
)
