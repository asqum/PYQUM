
from setuptools import setup, find_packages

setup(
    name='qspp',
    # Below 'version' line is updated during the build, DO NOT manually edit it!
    version='1.0',
    license='BSD',
    author='shiau, LTH',
    author_email='shiau109@gmail.com, ufocrew@gmail.com',
    description='Qubit Signal Post-Processing',
    long_description='1. Digital Homodyne: Dual & Single port',

    zip_safe=False,
    include_package_data=True,
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scipy',
        'matplotlib'
    ],
)

