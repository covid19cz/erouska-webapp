<script>
import Duration from './Duration.svelte';
import { createEventDispatcher } from 'svelte';

const dispatch = createEventDispatcher();

export let durationFilter = 0;

</script>

Duration:
<input type="range" min="0" max="1200"
  bind:value={durationFilter}
  on:input={(()=> dispatch('change', durationFilter))}
  style="--min: 0; --max: 1200; --val: {durationFilter}"
  />
<p>
Minimal contact duration <Duration duration={durationFilter} />
</p>

<style>
[type='range'] {
  --range: calc(var(--max) - var(--min));
  --ratio: calc((var(--val) - var(--min))/var(--range));
  --sx: calc(.5*1.5em + var(--ratio)*(100% - 1.5em));
  margin: 0;
  padding: 0;
  width: 12.5em;
  height: 1.5em;
  background: transparent;
  font: 1em/1 arial, sans-serif;
  outline: none;
}
[type='range'], [type='range']::-webkit-slider-thumb {
  -webkit-appearance: none;
}
[type='range']::-webkit-slider-runnable-track {
  box-sizing: border-box;
  border: none;
  width: 12.5em;
  height: 0.25em;
  background: var(--range-track);
}
[type='range']::-webkit-slider-runnable-track {
  background: linear-gradient(var(--range-run), var(--range-run)) 0/var(--sx) 100% no-repeat var(--range-track);
}
[type='range']::-moz-range-track {
  box-sizing: border-box;
  border: none;
  width: 12.5em;
  height: 0.25em;
  background: var(--range-track);
}
[type='range']::-ms-track {
  box-sizing: border-box;
  border: none;
  width: 12.5em;
  height: 0.25em;
  background: var(--range-track);
}
[type='range']::-moz-range-progress {
  height: 0.25em;
  background: var(--range-run);
}
[type='range']::-ms-fill-lower {
  height: 0.25em;
  background: var(--range-run);
}
[type='range']::-webkit-slider-thumb {
  margin-top: -0.625em;
  box-sizing: border-box;
  border: none;
  width: 1.5em;
  height: 1.5em;
  border-radius: 50%;
  background:  var(--range-thumb);
}
[type='range']::-moz-range-thumb {
  box-sizing: border-box;
  border: none;
  width: 1.5em;
  height: 1.5em;
  border-radius: 50%;
  background:  var(--range-thumb);
}
[type='range']::-ms-thumb {
  margin-top: 0;
  box-sizing: border-box;
  border: none;
  width: 1.5em;
  height: 1.5em;
  border-radius: 50%;
  background: var(--range-thumb);
}
[type='range']::-ms-tooltip {
  display: none;
}

</style>
