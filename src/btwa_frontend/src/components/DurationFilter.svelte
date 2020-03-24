<script>
import Duration from './Duration.svelte';
import { createEventDispatcher } from 'svelte';

const dispatch = createEventDispatcher();

export let value = 0;
export let max = 0;
export let min = 0;

</script>

<label>Délka:</label>
<input type="range"
  min={min}
  max={max-1}
  bind:value={value}
  on:input={()=> dispatch('change', value)}
  style="--min: 0; --max: {max}; --val: {value}"
  />
<p>
Minimální délka setkání <Duration duration={value+1} />
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
