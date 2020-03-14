import mimeMap from '../../MIME_MAP.json';

export function guessTypeFromExtension(file) {
  let ext = file.name.split('.').pop();
  let mime = mimeMap[ext];
  if (ext) file.guessedType = mime;
  return mime;
}


export default function(file) {
  // no mime type was passed.... try guessing one from extension
  return (file.type == '') ? guessTypeFromExtension(file) : file.type;
}
