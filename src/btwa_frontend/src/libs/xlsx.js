import XLSX from 'xlsx';
import * as d3 from "d3";

export default function(file){
  return new Promise(function(res, rej){

      try {
        let data = XLSX.read(file.body, {type: 'binary'});
        res({
          name : file.name +'/' + name,
          json : d3.csvParse(XLSX.utils.sheet_to_csv(data.Sheets[data.SheetNames[0]]))
        });
      } catch(e) {
        rej (e);
      }
  });
}
