import os

from setuptools import setup, find_packages


setup(
    name='EasierDocker',
    version='1.0.0',
    author='weiensong',
    author_email='touer0018@gmail.com',
    description='A brief description of your package',  # todo
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/your_package_name',  # todo
    packages=find_packages(),
    install_requires=[
            'docker~=6.1.3',
    ],
    entry_points={
        'console_scripts': [
            'your_script_name = your_package_name.your_module:main',
        ],
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='easy, docker, docker sdk, python docker',
    # todo
    project_urls={
        'Bug Reports': 'https://github.com/yourusername/your_package_name/issues',
        'Source': 'https://github.com/yourusername/your_package_name',
    },
)
