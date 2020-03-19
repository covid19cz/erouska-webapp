# Mobilní rouška
_(COVID-19 Bluetooth Tracking App) - Web Application_

TBD

## Installation for developer

The project is designed for Python 3.6 and it's recommended to install all dependencies into `venv`.
Check [the cookbook](https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/)
for getting familiar with `venv`.

Frontend is built by [`npm`](https://www.npmjs.com/) - you have to have it installed.

When the app is running, you can try to upload [testing file](testdata/usertable.xls).

### Set-up venv

You can use `source install_local.sh` (bash) or `. install_local.fish` (Fish) prepared script.  
Or, do it by your own:

```bash
git checkout https://github.com/covid19cz/bt-tracing-webapp.git
cd bt-tracing-webapp

python3 -m venv env
source env/bin/activate # . env/bin/activate.fish for fish
```

### Configure ENVs

In general, these envs are needed for the application to run:

- **GOOGLE_APPLICATION_CREDENTIALS**: Path to Firebase Admin JSON credentials
- **FIREBASE_DB_URL**: URL of Firestore database
- **FIREBASE_STORAGE_BUCKET**: URL of Cloud Storage bucket
- **DATABASE_URI** (optional): Connection string for SQL database (if unset, defaults to SQLite)  

In case you have GCP credentials JSON file saved as `google-credentials.json` file in project root,
all envs are already set and you don't have to do anything.  
If you need to change them, do that in [`envs_local.sh`](envs_local.sh) file.

### Setup local DB 

Setup local DB (SQLite) for some username (you'll be asked for password):

```bash
./setup_local.sh username
```

You will need those credentials when using the app.

### Run it locally from console

```bash
./start_local.sh
```

When the app is running, just [open it in your web browser](http://localhost:5000).
