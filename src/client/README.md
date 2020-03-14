### EpiTrace

Pairing bluetooth id with phones for tracing human contacts during pandemic.

---

## Get started

Install the dependencies...

```bash
npm install
```

...then start [Rollup](https://rollupjs.org):

```bash
npm run dev
```

Navigate to [localhost:5000](http://localhost:5000). You should see your app running. Edit a component file in `src`, save it, and reload the page to see your changes.

By default, the server will only respond to requests from localhost. To allow connections from other computers, edit the `sirv` commands in package.json to include the option `--host 0.0.0.0`.


## Building and running in production mode

To create an optimised version of the app:

```bash
npm run build
```

You can run the newly built app with `npm run start`. This uses [sirv](https://github.com/lukeed/sirv), which is included in your package.json's `dependencies` so that the app will work when you deploy to platforms like [Heroku](https://heroku.com).


## Configuration

All required configuration is in `CONFIG.json`

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
