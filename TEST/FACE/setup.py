import io

from setuptools import find_packages, setup

# with io.open('README.md', 'rt', encoding='utf8') as f:
#     readme = f.read()

setup(
    name='pyqum',
    version='1.0.1',
    url='',
    license='BSD',
    maintainer='Quela team',
    maintainer_email='qubitcool@gmail.com',
    description='Q Measurement App',
    #long_description=readme,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'numpy',
        'flask',
        'geocoder',
        'scrypt',
        'pyvisa',
        'nidaqmx',
        'colorama',
        'si-prefix',
        'typed-ast',
        'peakutils',
        'netifaces',
        'flask-ext',
        'Flask-NoExtRef',
        'keyboard',
        'matplotlib'
    ],
    extras_require={
        'test': [
            'pytest',
            'coverage',
        ],
    },
)
