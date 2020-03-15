<script>
import { contacts, phones } from './store.js';

import Dropzone from './Dropzone.svelte';
import Contacts from './Contacts.svelte';

</script>

<Dropzone>

  <header>
    <svg>
      <use xlink:href="icons.svg#logo" />
    </svg>
    <h1>EpiTrace</h1>
    <label class="button" for="uploadfile">Load file</label>
  </header>

  <main>
    {#if $contacts}
     <Contacts data={$phones || $contacts} />
    {:else}
      <aside class="upload">

        <h2>Drop file to upload</h2>
        <p>or use the dialog</p>
        <label class="button" for="uploadfile">Load file</label>
      </aside>
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
  background: var(--ui-header-background);
  color: var(--ui-header-color);
}
header h1 {
  flex-grow: 2;
  font-size: 1.5rem;
  font-weight: bold;
}
header svg {
  fill: var(--ui-header-color);
  width: calc( var(--ui-header-height) - 1rem );
  height: calc( var(--ui-header-height) - 1rem );
  margin-right: 1rem;
}
header .button:hover {
  background:  var(--ui-header-color);
  border: 1px solid  var(--ui-header-color);
  color: var(--ui-header-background);
}
main {
  position: fixed;
  left: 0;
  top: var(--ui-header-height);
  bottom: 0;
  right: 0;
}
aside {
  position: fixed;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  background: var(--theme-highlight);
  color: var(--theme-highlight-color);
  border-radius: 2rem;
}
.upload {
  padding: 4rem 2rem;
  text-align: center;
  min-width: 50%;
}
.upload > * {
  margin: 1rem 0;
}

</style>
