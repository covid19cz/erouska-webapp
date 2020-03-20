<script>
import {
  ENCOUNTER_TO,
  ENCOUNTER_FROM,
  ENCOUNTER_ID,
  INFECTED,
  DURATION,
  PHONE_NUMBER
} from '../CONFIG.json';

import { changeStatus, patient } from './store.js';

import { scaleLinear } from 'd3';
import dayjs from 'dayjs';

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
let timeScale = null;
let timeDuration = null;

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

  // scale for duration bar size
  durationScale = scaleLinear()
    .domain([dMin, dMax])
    .range([0,100]);

  timeMax = (new Date).valueOf(); // set today by default
  timeMin = tMin;

  // scale for timeline start
  timeScale = scaleLinear()
    .domain([tMin, tMax])
    .range([0,100]);

  // scale for timeline width
  timeDuration = scaleLinear()
    .domain([0, tMax-tMin])
    .range([0,100]);

  return filtered;
}


</script>

<div class="person">
  Contact history for {$patient.phone}
  <strong class="status {$patient.status}">{$patient.status}</strong>
  {#if $patient.status == 'infected'}
    <button class="button" on:click={() => changeStatus($patient.fuid, 'cured')}>Mark as Cured</button>
  {:else}
    <button class="button" on:click={() => changeStatus($patient.fuid, 'infected')}>Mark as Infected</button>
  {/if}
</div>

<div class="filters">
  <div class:active={durationFilter > 0}>
    <DurationFilter value={durationFilter} max={durationMax/1000} on:change={e => durationFilter = e.detail} />
  </div>
  <div class:active={timeFilter > timeMin} >
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
                <div class="timeline-indicator"
                  style="left: {timeScale(new Date(item[ENCOUNTER_FROM]).valueOf())}%;
                          width: {timeDuration(item[DURATION])}%"></div>
                <a href="tel:{item[col]}" class="button">{item[col]}</a>
              </td>

            {:else if col == ENCOUNTER_FROM}
              <td>
                {dayjs(item[col]).format('DD. MMM hh:mm:ss')}
              </td>

            {:else if col == ENCOUNTER_TO}
              <td>
                {dayjs(item[col]).format('DD. MMM hh:mm:ss')}
              </td>
            {:else if col == DURATION}
              <td class="duration">
                <div class="duration-scale" style="width: {durationScale(item[DURATION])}%"></div>
                <Duration duration={item[col]/1000} />
              </td>
            {:else if col == INFECTED}
              <td class:infected={item[col] == true}>{item[col]}</td>

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
    padding: 0 1rem 1rem;
  }
  .table {
    position: relative;
    border-spacing: 1px .6rem;
  }
  .person {
    position: absolute;
    left: 0;
    top: 0;
    right: 0;
    height: 2rem;
    text-align: center;
    font-size: 1.2rem;
    padding: .5rem 2rem;
  }
  .filters {
    position: absolute;
    left: 0;
    top: 2rem;
    right: 0;
    height: 8rem;
    display: flex;
    justify-content: space-between;
    padding: .5rem;
  }
  .filters > div {
    width: 49%;
    border: var(--box-border);
    margin:  .5rem;
    padding: 1rem;
    border-radius: var(--box-radius);
    flex-grow: 1;
  }
  .filters > div.active {
    box-shadow: 10px 10px 10px 0 rgba(0,0,0,.1);
  }
  .status {
    padding: .2rem 1rem;
    display: inline-block;

  }
  .infected {
    background: #F00;
    color: #FFF;
  }
  .actions {
  }
  .timeline-indicator {
    margin-top: -1rem;
    position: absolute;
    height: .3rem;
    min-width: 1%;
    background: var(--theme-highlight);
    border-radius: 1rem;
    opacity: .3;
  }
  .table tr:hover td .timeline-indicator   {
    opacity: 1;
  }
</style>
