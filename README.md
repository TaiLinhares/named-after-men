# Plants


## Setup

### Set virtual environment

https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment
https://docs.python.org/3/tutorial/venv.html


#### in anaconda prompt

// Check version, installed packages, and current environment
py --version
py -m  pip list
where python

// If virtualenv package not installed (one of two)
py -m pip install virtualenv
py -m pip install --user virtualenv

// Install environment in the project root folder
cd C:\Users\taian\Documents\Arts\Project\named_after_Men\Plants
py -m venv venv

### OR Activate conda in vscode
C:/Users/taian/Anaconda3/Scripts/activate
conda activate base

### Activate/Deactivate virtual environment (cmd, powershell or Anaconda prompt)
venv\Scripts\activate
deactivate


### Install Packages (Anaconda prompt with venv activated)
py -m pip install package-name


### Pythonic
https://pypi.org/project/black/
https://pypi.org/project/pycodestyle/