<script>
import { ENCOUNTER_TO, ENCOUNTER_FROM, ENCOUNTER_ID, PHONE_NUMBER } from './CONFIG.json';

import DurationFilter from './components/DurationFilter.svelte';


export let data = [];

let durationFilter = 0;
let focusContact = null;

$: d = applyFilter(data, durationFilter);

function applyFilter(data, durationFilter) {
  let filtered = data;
  if (durationFilter > 0) {
    filtered = data.filter(d => {
      return (new Date(d[ENCOUNTER_TO])).valueOf() - (new Date(d[ENCOUNTER_FROM])).valueOf() > durationFilter*1000;
    })
  }

  return filtered;
}

</script>
<h3>Filters</h3>
<div>
  <DurationFilter durationFilter={durationFilter} on:change={e => durationFilter  = e.detail} />
</div>

{#if d && d.length > 0}
  <table>
    <tr>
      {#each Object.keys(d[0]) as col}
        <th>{col}</th>
      {/each}
    </tr>

    {#each d as item}
      <tr
        on:mouseover={() => focusContact = item[ENCOUNTER_ID] }
        class:active={item[ENCOUNTER_ID] == focusContact}>
        {#each Object.keys(item) as col}
          <td>
            {#if col == PHONE_NUMBER}
              <a href="tel:{item[col]}" class="button">{item[col]}</a>
            {:else}
              {item[col]}
            {/if}

          </td>
        {/each}
      </tr>
    {/each}
  </table>
{:else}
  <div>
    No data.
  </div>
{/if}

<style>

  table {
    width: 100%;
  }
  tr th,
  tr td {
    padding: .2rem;
    font-size: .8rem;
  }

  tr th {
    background: var(--tr-odd);
  }
  tr:nth-child(even)  td {
    background: var(--tr-even);
  }
  tr:nth-child(odd)  td {
    background: var(--tr-odd);
  }
  tr.active td {
    background: var(--tr-active);
  }

  .phone {

  }
</style>
