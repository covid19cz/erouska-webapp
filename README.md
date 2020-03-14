COVID-19 Bluetooth Tracking App - Web Application

TBD

# Installation

The project is designed for Python 3.7 and it's recommended to install all dependencies into `venv`.
Check [the cookbook](https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/)
for getting familiar with `venv`.

Frontend is built by [`npm`](https://www.npmjs.com/) - you have to have it installed.

When the app is running, you can try to upload [testing file](testdata/usertable.xls).

## Bash, Fish

You can use `source install_local.sh` (bash) or `. install_local.fish` (Fish) prepared script.  
Or, do it by your own:

```bash
git checkout https://github.com/covid19cz/bt-tracing-webapp.git
cd bt-tracing-webapp

python3 -m venv env
source env/bin/activate # . env/bin/activate.fish for fish

cd src/btwa_frontend \
    && npm i \
    && npm run build \
    && cd ../..

pip install .
covid19-btwa
```

When the app is running, just [open it in your web browser](http://localhost:8080).

## IDE

Checkout the REPO from your favorite IDE and open the project. If you used `venv`, don't forget to setup it in the IDE or it will report
you don't have installed proper dependencies!

## Frontend config

Settings for frontend is in [CONFIG.json](src/btwa_frontend/CONFIG.json).  
You probably don't want to change it.

```
{
  // server url - can be empty if running on the same machine
  "SERVER" : "",
  // POST request endpoint
  // submits array of BT IDs
  "GET_PHONE_NUMBERS" : "fakePhones.json"
  // table column mapping
  "ENCOUNTER_FROM" : "Encounter_from",  
  "ENCOUNTER_TO" : "Encounter_to",
  "ENCOUNTER_ID" : "Encounter_BT_id",
  "PHONE_NUMBER" : "Phone_Number",
}
```
