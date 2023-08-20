import Hover from 'https://unpkg.com/wavesurfer.js@7/dist/plugins/hover.esm.js';
// tranformer le fichier en module

console.log('Hello World');

function toggleList(elemId){
    document.getElementById(elemId).classList.toggle('hidden');
}

function call(){
    let iniObj = {	
        method: 'POST',
        headers: { 
            'Content-Type': 'text/plain',
            'Accept': ' text/plain',
            'Referer': 'origin'
        },
        body: "iwantfigure"
    };

    fetch( "http://127.0.0.1:5000/", iniObj )
    .then( response => {
        if (response.ok){
            return response.text()
        } else{
            console.error(response.status, response.statusText)
        }
    })
    .then( data => {
        console.log(data);
        // include_fig(data);
    })
    .catch( err => { 
        console.log("login rejected : ", err);
        // Checking if this is an HTTP error
        if (err.status && err.response) {
            if (err.status === 401) {
                err.message = 'Access denied'
            }
        } else {
            throw err
        }
    })
}

function sendPath (inputEl) {
    console.log("value is ", inputEl.value);
    // Array.from(input.files);
}

function includeFile() {
    const wavesurfer = WaveSurfer.create({
        container: '#waveform',
        height: 256,
        // waveColor: '#114488',
        // progressColor: '#665588',
        normalize: true,
        minPxPerSec: 10,
        cursorWidth: 1,
        url: 'http://127.0.0.1:5000/file',
        // sampleRate: 8000,
        plugins: [
            Hover.create({
                lineColor: '#ff0000',
                lineWidth: 1,
                labelBackground: '#555',
                labelColor: '#fff',
                labelSize: '11px',
            }),
        ],
    })

    // Initialize the Timeline plugin
    // wavesurfer.registerPlugin(TimelinePlugin.create());
    
    wavesurfer.on(
        'interaction', 
        () => {wavesurfer.play()}
    );
}


