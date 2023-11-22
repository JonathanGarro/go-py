from setuptools import setup

setup(
    name='ifrc_go_py',
    version='0.0.1',
    description='A library for working with IFRC GO data.',
    author='Jonathan Garro',
    author_email='jonathan.garro@gmail.com',
    packages=['ifrc_go_py'],
    install_requires=['requests']
    )