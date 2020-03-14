<script>
import { contacts, phones } from './store.js';

import Dropzone from './Dropzone.svelte';
import Contacts from './Contacts.svelte';

</script>

<Dropzone>

  <header>
    <h1>EpiTrace</h1>
    <label class="button" for="uploadfile">Choose a file</label>
  </header>

  <main>
    {#if $contacts}
     <Contacts data={$phones || $contacts} />
    {/if}
  </main>

</Dropzone>

<style>

header {
  position: fixed;
  left: 0;
  top: 0;
  right: 0;
  height: var(--ui-header-height);
  display: flex;
  align-items: center;
  padding: .5rem;
  background: var(--theme-background-dark);
}
header h1 {
  flex-grow: 2;
  font-size: 1.5rem;
  font-weight: bold;
}
main {
  position: fixed;
  left: 0;
  top: var(--ui-header-height);
  bottom: 0;
  right: 0;
}

</style>
