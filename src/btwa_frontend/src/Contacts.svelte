<script>
import {
  ENCOUNTER_TO,
  ENCOUNTER_FROM,
  ENCOUNTER_ID,
  DURATION,
  PHONE_NUMBER
} from '../CONFIG.json';

import { scaleLinear } from 'd3';

import Duration from './components/Duration.svelte';
import DurationFilter from './components/DurationFilter.svelte';
import TimeFilter from './components/TimeFilter.svelte';


export let data = [];

let focusContact = null;

let durationFilter = 0;
let durationMax = 0;
let durationScale = null;

let timeFilter = 0;
let timeMin = 0;
let timeMax = 0;

$: d = applyFilter(data, durationFilter, timeFilter);


// filter and calculate full ranges
function applyFilter(data, minDuration, minTime) {
  let filtered = data;
  let dMin = 0;
  let dMax = 0;
  let tMin = undefined;
  let tMax = undefined;

  // apply time and duration filters
  filtered = data.filter(d => {
    const from = new Date(d[ENCOUNTER_FROM]).valueOf();
    const to = new Date(d[ENCOUNTER_TO]).valueOf();

    dMin = Math.min(dMin, d[DURATION]);
    dMax = Math.max(dMax, d[DURATION]);

    tMin = (tMin) ? Math.min(tMin, from) : from;
    tMax = (tMax) ? Math.max(tMax, to) : to;

    return (
      from >= minTime
      && ((minDuration > 0) ? d[DURATION] > minDuration*1000 : true)
    )
  });

  durationMax = dMax;

  durationScale = scaleLinear()
    .domain([dMin, dMax])
    .range([0,100]);

  timeMax = tMax;
  timeMin = tMin;


  return filtered;
}

</script>

<div class="filters">
  <div>
    <DurationFilter value={durationFilter} max={durationMax/1000} on:change={e => durationFilter = e.detail} />
  </div>
  <div>
    <TimeFilter value={timeMin} min={timeMin} max={timeMax} on:change={e => timeFilter = e.detail} />
  </div>
</div>
<div class="scroll">
{#if d && d.length > 0}
  <table class="table">
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
    margin: 1rem;
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
