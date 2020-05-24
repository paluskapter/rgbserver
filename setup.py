from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='rgbserver',
    version='0.0.1',
    description='RGB strip controller for Raspberry PI with REST API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/paluskapter/rgbserver',
    author='Peter Paluska',
    author_email='paluskapter@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
        'Typing :: Typed'
    ],
    keywords='raspberry pi neopixel ws2812 rest api',
    packages=find_packages(exclude="tests"),
    python_requires='>=3, <4',
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'run=app:run',
        ],
    },
)
