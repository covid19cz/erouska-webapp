<script>
import { onMount, createEventDispatcher } from 'svelte';
import importFile from './libs/importFile.js';
import { contacts } from './store.js';


window.dragLocalOrigin = false;

let dropzone = null;
let dropTimer = null;
let dragover = false;
let dropped = [];
let upload = null;

function processFiles (transfer) {
  importFile(transfer.files)
    .then(data => { contacts.set(data.json) });
}

onMount(() => {

  dropzone.addEventListener('dragenter', (e) => {

    if(window.dragLocalOrigin) return false;

    dragover = true;
    dropped = [];
  });

  dropzone.addEventListener('dragover', (e) => {
    if(window.dragLocalOrigin) return false;

    e.stopPropagation();
    e.preventDefault();
    e.dataTransfer.dropEffect = 'copy';
    clearTimeout(dropTimer);
  });

  dropzone.addEventListener('dragleave', (e) => {

    if(window.dragLocalOrigin) return false;

    clearTimeout(dropTimer);
    dropTimer = setTimeout(()=>{
      dragover = false;
      dropped = [];
    },150);
  });

  dropzone.addEventListener('drop', (e) => {

    e.stopPropagation();
    e.preventDefault();

    if(window.dragLocalOrigin) return false;

    dragover = false;
    dropped = [];
    processFiles(e.dataTransfer);

  });

});

</script>

<div bind:this={dropzone} class="dropzone">

  <slot />

  <input type="file" name="uploadfile" id="uploadfile" bind:this={upload} on:change={() => processFiles({ files : upload.files })} />

  {#if dragover}
    <div class="dragover">
      <h2>Drop files to process</h2>
    </div>
  {/if}
</div>



<style>
  .dropzone {
    position: fixed;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    overflow: auto;
  }
  .dragover {
    position: fixed;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    overflow: hidden;
    background: var(--overlay-background);
    color: #FFF;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  input[type="file"] {
    width: 0.1px;
    height: 0.1px;
    opacity: 0;
    overflow: hidden;
    position: absolute;
    z-index: -1;
  }

</style>
