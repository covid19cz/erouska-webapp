import { csvParse } from 'd3';
import fileType from './fileTypes.js';
import fileReader from './fileReader.js';
import xlsx from './xlsx.js';
import csv from './csv.js';


function parseFile(file) {
  // determin file mime
  let type = fileType(file);

  switch ( type )  {

    case 'application/vnd.oasis.opendocument.spreadsheet':
    case 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
    case 'application/vnd.ms-excel':
      return  fileReader(file, 'binary').then(xlsx);

    case 'text/csv':
      return fileReader(file).then(csv);

    default:
      return Promise.reject('Unsupported file');
  }

}


export default function(files) {
  // by default we support just 1 file per upload
  let file = files[0];
  let promised = [];

  return parseFile(file);
}
