from setuptools import setup

from txr import (
    __package_name__,
    __author__,
    __author_email__,
    __license__,
    __url__,
    __version__,
    __description__,
)

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3',
]

__readme__ = open('README.rst', encoding="utf-8").read()
__readme_type__ = 'text/x-rst'

setup(
    name=__package_name__,
    version=__version__,
    author=__author__,
    author_email=__author_email__,
    license=__license__,
    url=__url__,
    long_description=__readme__,
    long_description_content_type=__readme_type__,
    description=__description__,
    classifiers=classifiers,
    py_modules=[__package_name__],
    entry_points={'console_scripts': ['txr = txr:main', ], },
    extras_require={
        "crypto": ['cryptography'],
    },
    python_requires=">=3.6.0",
)