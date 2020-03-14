<script>
import Duration from './Duration.svelte';
import { createEventDispatcher } from 'svelte';

const dispatch = createEventDispatcher();

export let durationFilter = 0;

</script>

<label>Duration:</label>
<input type="range" min="0" max="1200"
  bind:value={durationFilter}
  on:input={(()=> dispatch('change', durationFilter))}
  style="--min: 0; --max: 1200; --val: {durationFilter}"
  />
<p>
Minimal contact duration <Duration duration={durationFilter} />
</p>

<style>
label {
  display: block;
  margin: .5rem 0;
  font-size: 1rem;
  font-weight: bold;
}
p {
  font-size: .8rem;
}
[type='range'] {
  --range: calc(var(--max) - var(--min));
  --ratio: calc((var(--val) - var(--min))/var(--range));
  --sx: calc(.5*var(--range-thumb-size) + var(--ratio)*(100% - var(--range-thumb-size)));
  margin: 0;
  padding: 0;
  width: 100%;
  height: var(--range-thumb-size);
  border-radius: var(--range-thumb-size);
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
  width: 100%;
  height:var(--range-thumb-size);
  background: var(--range-track);
  border-radius: var(--range-thumb-size);
}
[type='range']::-webkit-slider-runnable-track {
  background: linear-gradient(var(--range-run), var(--range-run)) 0/var(--sx) 100% no-repeat var(--range-track);
}
[type='range']::-moz-range-track {
  box-sizing: border-box;
  border: none;
  width: 100%;
  height: var(--range-thumb-size);
  background: var(--range-track);
  border-radius: var(--range-thumb-size);
}
[type='range']::-ms-track {
  box-sizing: border-box;
  border: none;
  width: 100%;
  height: var(--range-thumb-size);
  background: var(--range-track);
  border-radius: var(--range-thumb-size);
}
[type='range']::-moz-range-progress {
  height: var(--range-thumb-size);
  background: var(--range-run);
}
[type='range']::-ms-fill-lower {
  height: var(--range-thumb-size);
  background: var(--range-run);
}
[type='range']::-webkit-slider-thumb {
  box-sizing: border-box;
  border: none;
  width: var(--range-thumb-size);
  height: var(--range-thumb-size);
  border-radius: 50%;
  background:  var(--range-thumb);
}
[type='range']::-moz-range-thumb {
  box-sizing: border-box;
  border: none;
  width: var(--range-thumb-size);
  height: var(--range-thumb-size);
  border-radius: 50%;
  background:  var(--range-thumb);
}
[type='range']::-ms-thumb {
  margin-top: 0;
  box-sizing: border-box;
  border: none;
  width: var(--range-thumb-size);
  height: var(--range-thumb-size);
  border-radius: 50%;
  background: var(--range-thumb);
}
[type='range']::-ms-tooltip {
  display: none;
}

</style>
