from setuptools import setup, find_packages

setup(
    name='easier-docker',
    version='2.2.2',
    author='EnSong Wei',
    author_email='touer0018@gmail.com',
    description='Configure your container image information more easily in python, allowing the container in docker '
                'to execute the configured program you want to execute',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/touero/easier-docker',
    packages=find_packages(),
    license='Apache License 2.0',
    install_requires=[
        'docker~=6.1.3',
        'setuptools~=68.2.0',
        'PyYAML~=6.0.1'
    ],
    entry_points={
        'console_scripts': [
            'easier-docker=easierdocker.__main__:main',
        ],
    },
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    keywords='easy, docker, docker sdk, python docker',
    project_urls={
        'Bug Reports': 'https://github.com/touero/easier-docker/issues',
        'Source': 'https://github.com/touero/easier-docker',
    },
)
