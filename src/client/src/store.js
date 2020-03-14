import { writable, derived } from 'svelte/store';

import { ENCOUNTER_ID, SERVER, GET_PHONE_NUMBERS, PHONE_NUMBER } from './CONFIG.json';


export const contacts = writable(null);


// contacts with all phone numbers fetched
export const phones = derived(contacts, async (contacts, set) => {
  if (!contacts) return null;

  const ids = contacts.map(c => c[ENCOUNTER_ID]);

  // fetch phone numbers from the server
	return fetch(SERVER + GET_PHONE_NUMBERS)
    .then(response => response.json())
    .then(phones => {
      set(contacts.map(c => {
        c[PHONE_NUMBER] = phones[c[ENCOUNTER_ID]] || undefined;
        return c;
      }));
    });

}, null);
