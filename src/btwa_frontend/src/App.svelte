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
  display: flex;
  padding: .5rem;
  background: #CCC;
}
header h1 {
  flex-grow: 2;
}

</style>
