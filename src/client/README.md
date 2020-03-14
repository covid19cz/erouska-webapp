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



## Building and running in production mode

To create an optimised version of the app:

```bash
npm run build
```

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
