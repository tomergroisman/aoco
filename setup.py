from setuptools import setup


with open('requirements.txt') as f:
    requirements = f.read().splitlines()


setup(
    name='aoco',
    version='1.0',
    description='Advent of Code runner cli application',
    author='Tomer Groisman',
    packages=["aoco"],
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'aoco = aoco.__main__:main',
        ],
    },
    include_package_data=True
)
