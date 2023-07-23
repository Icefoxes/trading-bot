import setuptools


with open("README.md", "r") as fh:
  long_description = fh.read()


setuptools.setup(
  name="hades-bot",
  version="0.0.1",
  author="Gary Guo",
  author_email="gary.guo.china@gmail.com",
  description="bitcoin trading bot",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/Icefoxes/trading-bot",
  packages=setuptools.find_packages(where='.', exclude=['hades*', 'test*']),
  install_requires=['python-okx', 'pandas', 'websockets', 'requests', 'binance-futures-connector'],
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)
