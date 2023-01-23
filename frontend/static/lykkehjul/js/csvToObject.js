function readFile() {
  // Hent opplastet fil
  const [file] = document.getElementById('InputFile').files;

  // Les innhold i fil
  const reader = new FileReader();
  reader.addEventListener("load", () => {
    // Hent resultat fra FileReader
    let csvString = reader.result;
    // Konverter til array
    let arr = "";
    if (csvString.includes("\r\n")){
      arr = csvString.split('\r\n');
    }
    else {
      arr = csvString.split('\n');
    }
    // Fjern første element
    // arr.shift();

    // Konverter til objekt
    let object = {};

    for (const data of arr) {
      let value = parseInt(data.split(',')[1]);
      if (isNaN(value)) {value = 1};
      object[data.split(',')[0]] = value;

    };
    // Sletter tullete ting
    delete object[""]
    delete object[" "]

    // Lag hjulet
    for (const name in object) {
      const data   = {};
      data.tickets = object[name];
      data.start   = 0;
      data.end     = 0;
      candidates[name] = data
    }

    createWheel(wheelsize);

  }, false);

  // Har ikke peiling på hva dette gjør
  if (file) {
    reader.readAsText(file);
  }
}

// Legg til lytter for knapp 
//Funker ikke, bruker onclick istedet
document.getElementById('BtnUpload').addEventListener("onclick", readFile);

