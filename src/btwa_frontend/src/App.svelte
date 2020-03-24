<script>
import { phones, error, getUser } from './store.js';

import Dropzone from './Dropzone.svelte';
import Contacts from './Contacts.svelte';

let searchDialog = true;
let searchNumber = '';

function search() {
  if (searchNumber != '') getUser(searchNumber)
    .then(data => {
      searchDialog = false;
    });
}


</script>

<Dropzone>

  <header>
    <svg>
      <use xlink:href="res/icons.svg#logo" />
    </svg>
    <h1>EpiTrace</h1>
    <label class="button" on:click={() => searchDialog = true}>Vyhledat číslo</label>
    <!--label class="button" for="uploadfile">Load file</label-->
  </header>

  <main>
    {#if $phones}
     <Contacts data={$phones} />
    {/if}
  </main>

  {#if searchDialog}
    <div class="overlay">
      <aside class="modal">
        <h2>Vyhledat uživatele</h2>
        {#if $error}
        <div class="error">{$error}</div>
        {/if}
        <input class="search" type="text" bind:value={searchNumber} placeholder="Phone number" /><br/>
        <button class="button" on:click="{search}">Vyhledat</button>
      </aside>
    </div>
  {/if}

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
  padding: .5rem 2rem;
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
  background-image: linear-gradient(var(--theme-background-light), var(--theme-background-dark));
  color: var(--theme-color);
  border-top-left-radius: 2rem;
  border-top-right-radius: 2rem;
  box-shadow: 0px -10px 40px 0 rgba(0,0,0,.4);
}

.overlay {
  position: fixed;
  left: 0;
  top: 0;
  right: 0;
  bottom: 0;
  z-index: 10000;
  background-color: rgba(255,255,255,.8);

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
.modal {
  padding: 4rem 2rem;
  text-align: center;
  min-width: 50%;
}
.modal > * {
  margin: 1rem 0;
}
.error {
  background: #F00;
  color: #FFF;
  border-radius: 2rem;
  padding: .5rem 1rem;
}

.search {
  background: #FFF;
  border-radius: 2rem;
  border: 0;
  padding: .5rem 1rem;
  width: 25vw;
}

</style>
