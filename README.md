# Plants


## Setup

### Handling secrets and environment variables

Copy the `.env.template` file and rename it to `.env` add your secrets here. These values will then be loaded as environment variables and used to create a config object in the config package.

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

### Pythonic Linting

This project is linted using both [Black](https://pypi.org/project/black/) and [Pycodestyle(https://pypi.org/project/pycodestyle/). Both can be installed locally and ran with the following commands.

```sh
black .
pycodestyle .
```

Configuration for pycodestyle can be found in the `./setup.cfg` file. The linters will also run as github actions when code is pushed to Github.