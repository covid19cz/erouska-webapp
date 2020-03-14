<script>

export let duration = 0;

$: readable = secondsToHms (duration);

function secondsToHms(d) {
    d = Number(d);

    var h = Math.floor(d / 3600);
    var m = Math.floor(d % 3600 / 60);
    var s = Math.floor(d % 3600 % 60);

    var duration = {};
    if (h > 0) duration.h = h + (h == 1 ? ' hour ' : ' hours ');
    if (m > 0 ) duration.m = m + (m == 1 ? ' minute ' : ' minutes ');
    if (s > 0) duration.s = s + (s == 1 ? ' second' : ' seconds');

    return Object.keys(duration).map(d => duration[d]).join(',');
}


</script>

{readable}
