# Plants


## Setup

### Set virtual environment

https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment
https://docs.python.org/3/tutorial/venv.html

#### in anaconda prompt

```sh
// Check version, installed packages, and current environment
py --version
py -m  pip list
where python

// If virtualenv package not installed (one of two)
py -m pip install virtualenv
py -m pip install --user virtualenv

// Install environment in the project root folder
cd C:\Users\taian\Documents\Arts\Project\named_after_Men\Plants
python -m venv venv
```

### OR Activate conda in vscode
```sh
C:/Users/taian/Anaconda3/Scripts/activate
conda activate base
```

### Activate/Deactivate virtual environment (cmd, powershell or Anaconda prompt)
```sh
venv\Scripts\activate
// or on linux
source venv/bin/activate
deactivate
```


### Install Packages (Anaconda prompt with venv activated)
```sh
py -m pip install package-name
```

### Update requirements txt
```sh
pip3 freeze > requirements.txt
```

### Pythonic
https://pypi.org/project/black/
https://pypi.org/project/pycodestyle/