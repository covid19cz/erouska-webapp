<script>
import {
  ENCOUNTER_TO,
  ENCOUNTER_FROM,
  ENCOUNTER_ID,
  DURATION,
  PHONE_NUMBER
} from '../CONFIG.json';

import { scaleLinear } from 'd3';

import DurationFilter from './components/DurationFilter.svelte';
import Duration from './components/Duration.svelte';


export let data = [];

let durationFilter = 0;
let durationMax = 0;
let focusContact = null;
let durationScale = null;

$: d = applyFilter(data, durationFilter);

function applyFilter(data, durationFilter) {
  let filtered = data;
  let min = 0;
  let max = 0;

  filtered = data.filter(d => {
    min = Math.min(min, d[DURATION]);
    max = Math.max(max, d[DURATION]);
    return (durationFilter > 0) ? d[DURATION] > durationFilter*1000 : true;
  });
  durationMax = max;
  durationScale = scaleLinear()
    .domain([min, max])
    .range([0,100]);

  return filtered;
}

</script>

<div class="filters">
  <div>
    <DurationFilter value={durationFilter} max={durationMax/1000} on:change={e => durationFilter  = e.detail} />
  </div>
</div>
<div class="scroll">
{#if d && d.length > 0}
  <table>
    <tr>
      {#each Object.keys(d[0]) as col}
        <th>{col.replace(/_/g, ' ')}</th>
      {/each}
    </tr>

    {#each d as item}
      <tr
        on:mouseover={() => focusContact = item[ENCOUNTER_ID] }
        class:active={item[ENCOUNTER_ID] == focusContact}>
        {#each Object.keys(item) as col}

            {#if col == PHONE_NUMBER}
              <td class="actions">
                <a href="tel:{item[col]}" class="button">{item[col]}</a>
              </td>

            {:else if col == DURATION}
              <td class="duration">
                <div class="duration-scale" style="width: {durationScale(item[DURATION])}%"></div>
                <Duration duration={item[col]/1000} />
              </td>

            {:else}
              <td>{item[col]}</td>
            {/if}

        {/each}

      </tr>
    {/each}
  </table>
{:else}
  <div>
    No data.
  </div>
{/if}
</div>
<style>

  .scroll {
    position: absolute;
    left: 0;
    top: 10rem;
    right: 0;
    bottom: 0;
    overflow: auto;
  }
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
    padding: .5rem;
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

  tr td.actions {
    text-align: center;
  }
  tr td.duration {
    position: relative;
  }
  tr td .duration-scale {
    position: absolute;
    left: 0;
    top: 0;
    width: 0;
    height: 100%;
    background: var(--tr-scale);
    pointer-events: none;
    user-select: none;
    z-index: -1;
  }

  .filters {
    position: absolute;
    left: 0;
    top: 0;
    right: 0;
    height: 10rem;
    display: flex;
    justify-content: space-between;
    padding: .5rem;
  }
  .filters > div {
    max-width: 32%;
    border: var(--box-border);
    margin:  0 1% 1%;
    padding: 1rem;
    border-radius: var(--box-radius);
    flex-grow: 1;
  }
</style>
