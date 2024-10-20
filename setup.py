from setuptools import setup, find_packages
import os

# Ensure README.md exists
readme_file = 'README.md'
if not os.path.exists(readme_file):
    raise FileNotFoundError(f"{readme_file} not found. Please create a README file.")

setup(
    name="flask-softdelete",
    version="0.2.0",
    description="A simple mixin for adding soft delete functionality to Flask-SQLAlchemy models",
    long_description=open(readme_file).read(),
    long_description_content_type='text/markdown',
    author="Mohamed Ndiaye",
    author_email="mintok2000@gmail.com",
    url="https://github.com/Moesthetics-code/flask-softdelete",
    packages=find_packages(),
    install_requires=[
        'Flask>=2.0.0',
        'Flask-SQLAlchemy>=2.5.0'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Framework :: Flask',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
