import * as d3 from "d3";

export default function(file){
  return new Promise(function(res, rej){
      try {
      let data = d3.csvParse(file.body);
      res({
        name : file.name,
        json : data,
      });
    } catch (e) {
      rej(e);
    }
  });
}
