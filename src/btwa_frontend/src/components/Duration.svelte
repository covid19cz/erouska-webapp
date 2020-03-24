<script>

export let duration = 0;

$: readable = secondsToHms (duration);

function secondsToHms(timestamp) {
  const duration = {};

  timestamp = Number(timestamp);

  // count days, hours, minutes and seconds
  var d = Math.floor(timestamp / 3600 / 24);
  var h = Math.floor(timestamp / 3600 % 24);
  var m = Math.floor(timestamp % 3600 / 60);
  var s = Math.floor(timestamp % 3600 % 60);

  if (d > 0) duration.d = d + (d == 1 ? ' den ' : ' dnů');
  if (h > 0) duration.h = h + (h == 1 ? ' hodina ' : ' hodin');
  if (m > 0 ) duration.m = m + (m == 1 ? ' minuta ' : ' minut');
  if (s > 0) duration.s = s + (s == 1 ? ' vteřina' : ' vteřin');

  // map object to , separated string
  return Object.keys(duration).map(d => duration[d]).join(', ');
}


</script>

{readable}
