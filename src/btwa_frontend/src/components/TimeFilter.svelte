<script>
import Duration from './Duration.svelte';
import { createEventDispatcher } from 'svelte';

const dispatch = createEventDispatcher();

export let value = 0;
export let max = 0;
export let min = 0;

</script>

<label>Časové okno:</label>

<input type="range"
  min={min}
  max={max}
  bind:value={value}
  on:input={()=> dispatch('change', value)}
  style="--min: {min}; --max: {max}; --val: {value}"
  />
<p>
Posledních <Duration duration={(max - value)/1000} />
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
</style>
