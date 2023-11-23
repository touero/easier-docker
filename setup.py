from setuptools import setup, find_packages


setup(
    name='easier_docker',
    version='1.0.0',
    author='weiensong',
    author_email='touer0018@gmail.com',
    description='A python package that makes it easier for you to use local docker.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/weiensong/easierdocker',
    packages=find_packages(),
    install_requires=[
            'docker~=6.1.3',
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='easy, docker, docker sdk, python docker',
    project_urls={
        'Bug Reports': 'https://github.com/weiensong/easier_docker/issues',
        'Source': 'https://github.com/weiensong/easierdocker',
    },
)
