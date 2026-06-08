from setuptools import find_packages, setup
from typing import List

def get_requirements():
    """
    This function will return list of requirements
    """
    requriement_list:List[str] = []

    try:
        with open('requirements.txt','r') as file:
            # Readd lines from the files
            lines = file.readlines()
            for line in lines:
                requriement = line.strip()
                # Ignore empty line and -e .
                if requriement and requriement!= '-e .':
                    requriement_list.append(requriement)
    except FileNotFoundError:
        print('requirements.txt file not found')

    return requriement_list

setup(
    name='NetworkSecurity',
    version='0.0.1',
    author='Shikhar Gupta',
    author_email='shikharjul01@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements()
)