COVID-19 Bluetooth Tracking App - Web Application

TBD

# Installation

The project is designed for Python 3.7 and it's recommended to install all dependencies into `venv`.
Check [the cookbook](https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/)
for getting familiar with `venv`.

## Bash, Fish

```bash
git checkout https://github.com/covid19cz/bt-tracing-webapp.git
cd bt-tracing-webapp

python3 -m venv env
source env/bin/activate # . env/bin/activate.fish for fish

pip install .
covid19-btwa
```

When the app is running, just [open it in your web browser](http://localhost:8080).

## IDE

Checkout the REPO from your favorite IDE and open the project. If you used `venv`, don't forget to setup it in the IDE or it will report
you don't have installed proper dependencies!
