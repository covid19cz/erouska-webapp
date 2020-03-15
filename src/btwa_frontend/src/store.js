import { writable, derived } from 'svelte/store';
import dayjs from 'dayjs';
import customParseFormat from 'dayjs/plugin/customParseFormat';

dayjs.extend(customParseFormat);

import {
  ENCOUNTER_TO,
  ENCOUNTER_FROM,
  ENCOUNTER_ID,
  DURATION,
  SERVER,
  GET_PHONE_NUMBERS,
  PHONE_NUMBER
} from '../CONFIG.json';


export const contacts = writable(null);


// contacts with all phone numbers fetched
export const phones = derived(contacts, async (contacts, set) => {
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

}, null);
