export default function(file, type = 'text', enc = 'UTF-8'){
  return new Promise(function(res, rej){

    let reader = new FileReader();
    switch(type){
      case 'text':
        reader.readAsText(file, enc);
        break;
      case 'binary':
        reader.readAsBinaryString(file);
        break;
      case 'buffer':
        reader.readAsArrayBuffer(file);
        break;
      default :
        rej('unknowntype', type);
        break;
    }


    reader.onload = (evt) => {
        file.body = evt.target.result;
        res(file);
    }

    reader.onerror = function (evt) {
      rej('parseError')
    }

  });
}
