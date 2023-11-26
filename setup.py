from setuptools import setup, find_packages

setup(
    name='easier-docker',
    version='2.0.0',
    author='weiensong',
    author_email='touer0018@gmail.com',
    description='It can create a container based on the local image. If the image does not exist, the image will be '
                'pulled down. If the container exists, it will be started directly. Then execute any service you want '
                'to execute in the container.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/weiensong/easierdocker',
    packages=find_packages(),
    install_requires=[
        'docker~=6.1.3',
        'setuptools~=68.2.0',
        'PyYAML~=6.0.1'
    ],
    entry_points={
        'console_scripts': [
            'easier-docker=easierdocker.config_run:main',
        ],
    },
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
