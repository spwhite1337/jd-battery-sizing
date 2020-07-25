from setuptools import setup, find_packages

setup(
    name='jd-battery-sizing',
    version='1.0',
    description='Battery Sizing for Dad',
    author='Scott P. White',
    author_email='spwhite1337@gmail.com',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'xlrd',
        'flask',
        'flask-wtf',
        'flask-sqlalchemy',
        'flask-migrate',
        'flask-login',
        'plotly',
        'dash',
        'ipykernel',
        'tqdm',
    ]
)
