from setuptools import setup

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ifrc_go_py',
    version='0.0.7',
    description='A library for working with IFRC GO data.',
    author='Jonathan Garro',
    author_email='jonathan.garro@gmail.com',
    project_urls={
        'GitHub': 'https://github.com/JonathanGarro/go-py',
    },
    license='MIT',
    packages=['ifrc_go_py'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'requests>=2.0.0', 
        'seaborn==0.12.2',
        'matplotlib==3.7.2',
        'geopandas==0.13.2',
        'pandas>=1.5.0'
    ]
    )