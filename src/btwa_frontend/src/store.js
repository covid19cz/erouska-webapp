import { writable, derived } from 'svelte/store';
import dayjs from 'dayjs';
import customParseFormat from 'dayjs/plugin/customParseFormat';

dayjs.extend(customParseFormat);

import {
  ENCOUNTER_TO,
  ENCOUNTER_FROM,
  ENCOUNTER_ID,
  INFECTED,
  DURATION,
  SERVER,
  GET_PHONE_NUMBERS,
  PHONE_NUMBER,
  CHANGE_USER_STATUS,
  GET_USER,
  GET_PROXIMITY
} from '../CONFIG.json';


export const patient = writable(null);

export const fileContents = writable(null);

export const phones = writable(null);

export const error = writable(null);


/*

// contacts with all phone numbers fetched
export const phones = derived(fileContents, async (contacts, set) => {
  if (!contacts) return null;

  const ids = contacts.map(c => c[ENCOUNTER_ID]);

  // fetch phone numbers from the server
	return fetch(SERVER + GET_PHONE_NUMBERS, {
    method: 'POST',
    credentials: 'same-origin',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(ids)
  })
    .then(response => response.json())
    .then(phones => {
      set(contacts.map(c => {
        c[ENCOUNTER_FROM] = dayjs(c[ENCOUNTER_FROM], 'DD/MM/YY hh:mm')
        c[ENCOUNTER_TO]= dayjs(c[ENCOUNTER_TO], 'DD/MM/YY hh:mm');
        c[DURATION] = (new Date(c[ENCOUNTER_TO])).valueOf() - (new Date(c[ENCOUNTER_FROM])).valueOf()
        c[PHONE_NUMBER] = phones[c[ENCOUNTER_ID]] || undefined;
        return c;
      }));
    });

}, null);*/


export function changeStatus (fuid, status) {

  error.set(null);

  return fetch(SERVER + CHANGE_USER_STATUS.replace('{fuid}', fuid), {
    method: 'POST',
    credentials: 'same-origin',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ status })
  });
}


export function getUser (phone) {

  error.set(null);

  return fetch(SERVER + GET_USER, {
    method: 'POST',
    body: JSON.stringify({ phone }),
    credentials: 'same-origin',
    headers: {
      'Content-Type': 'application/json'
    }
  })
    .then(response => {
      if (response.status !== 200) {
          throw new Error('Error processing request');
      } else {
        return response;
      }
    })
    .then(response => response.json())
    .then(user => {
      patient.set(Object.assign({ phone }, user));

      return fetch(SERVER + GET_PROXIMITY.replace('{fuid}', user.fuid),{
        method: 'GET',
        credentials: 'same-origin',
        headers: {
          'Content-Type': 'application/json'
        }
      })
        .then(response => {
          if (response.status !== 200) {
              throw new Error('Error processing request');
          } else {
            return response;
          }
        })
        .then(response => response.json())
        .then(data => {
          phones.set(data.map(d => {
            let c= {}
            c[ENCOUNTER_FROM] = d.start;
            c[ENCOUNTER_TO]= d.end;
            c[DURATION] = d.end - d.start;
            c[INFECTED] = d.infected;
            c[PHONE_NUMBER] = d.phone;
            return c;
          }));
        });
    })
    .catch(e => {
      error.set(e);
      throw new Error('no data fetched');
    });
}
