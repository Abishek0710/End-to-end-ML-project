from setuptools import find_packages,setup
from typing import  List



# creating a func that takes a file path as input and returns a list
# while calling requirements.txt below func is executed

HYPEN_E_DOT = '-e .'
def get_requirements(file_path:str)->List[str]:
    '''
    This function returns the list of requirements
    '''
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace('\n','') for req in requirements] # readlines will add \n after reading a line so we are handling that

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT) # we are ignoring -e . in setup file
    return requirements



setup(
name ='mlproject',
version = '0.0.1',
author = 'Abishek',
author_email = 'abishekrab101@gmail.com',
packages = find_packages(),
install_requires = get_requirements('requirements.txt')



)