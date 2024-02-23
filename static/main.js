// ajouter/supprimer/modifier les notes
// enregistrer les résultats/le projet
// enregistrer le midi
// afficher le graph
// save to excel ?
// https://wavesurfer-js.org/examples/#hover.js
var wavesurfer = null;
// var regionsPlugin = null;

function toggleList(elemId){
    document.getElementById(elemId).classList.toggle('hidden');
}


/**
 * Use the location entered in 'Project directory' field as the working directory. Retrieves list of files in the directory from the server. Populates the dropdown with files' name. Display a toast about the server's response.
 *
 * @returns {void}
 */
async function defineProjectDirectory() {
    const location = document.getElementById('project-directory').value;
    let data = await request_data("/files_list", "?location="+location);
    // console.log("data :", data);
    if(data.files.length > 0){
        displayToast(data.files.length + " wav files have been successfully loaded.");
        document.getElementById("project-directory").setAttribute("disabled", true);
        document.getElementById("project-directory-input").setAttribute("disabled", true);
        addFilesToDropdown(data.files);
    }
    else {
        displayToast("No wav files were found. Please verify the path you proposed.");
    }
}


async function saveData(fpath, regionsP) {
    let data = {
        name: fpath,
        notes: []
    };
    let regionArray = regionsP.getRegions();
    for (let r of regionArray){
        data.notes.push({
            start: r.start, 
            end: r.end
        });
    }
    data = JSON.stringify(data);
    const resp = await send_data("/file_notes", data);
    displayToast(resp=="ok" ? "Notes have been recorded for <code>"+document.getElementById("files-dropdown").value+"</code>" : "Error : Notes have not been recorded for <code>"+document.getElementById("files-dropdown").value+"</code>");

    return resp;
}

/**
 * Add files' name in the dropdown widget.
 *
 * @param {*} files
 */
function addFilesToDropdown(files){
    const dropdown = document.getElementById("files-dropdown");
    for(let file of files){
        let optionEl = document.createElement("option");
        optionEl.setAttribute("value", file);
        optionEl.innerHTML = file;
        dropdown.appendChild(optionEl);
    }
}

/**
 * 
 */
async function loadFile(){
    hideToast();
    const fname = document.getElementById("files-dropdown").value;
    if (fname.length > 0) {
        const fpath = document.getElementById("project-directory").value + fname; // attention au slash avant le nom du fichier("files-dropdown").value;
        let notes = await request_data("/file_notes", "?fpath="+fpath);
        // console.log("notes : ", notes);
        includeFile(fpath, notes);
    }
    return false;
}

/**
 * Creates a wavesurfer instance using the 'fpath' file.
 * Links 'Add Region' and 'Save notes' buttons to the file. 
 *
 * @param {String} fpath Full path of the audio file to work on.
 * @param {*} notes Notes data of the audio file.
 */
function includeFile(fpath, notes) {
    // Erreur, wavesurfer tente de faire un GET sur url (ne marche pas sur un fichier local)
    // document.getElementById("waveform").classList.remove("bg-stone-300", "h-64");
    // requeter les infos json du server
    // puis les utiliser pour ajouter les régions automatiquement
    if(wavesurfer !== null){
        // regions.clearRegions();
        wavesurfer.destroy();
        wavesurfer = null;
        // document.getElementById("waveform").innerHTML = "";
    }
    wavesurfer = WaveSurfer.create({
        container: '#waveform',
        height: 256,
        waveColor: '#78716C', // stone-500
        progressColor: '#44403C', // stone-700
        normalize: true,
        minPxPerSec: 250,
        // hideScrollbar: true,
        cursorWidth: 1,
        url: "http://127.0.0.1:5000/file?fpath="+fpath,
        // sampleRate: 8000,
        plugins: [
            // WaveSurfer.Minimap.create({
            //     height: 30,
            //     normalize: true,
            //     cursorWidth: 1,
            //     // the Minimap takes all the same options as the WaveSurfer itself
            // }),
            WaveSurfer.Timeline.create({
                // height: 20,
            }),
            // WaveSurfer.Regions.create({
            //     color: randomColor(),
            //     drag: true,
            //     start: 2,
            //     end: 3,
            // }),
        //     Hover.create({
        //         lineColor: '#ff0000',
        //         lineWidth: 1,
        //         labelBackground: '#555',
        //         labelColor: '#fff',
        //         labelSize: '11px',
        //     }),
        ],
    })

    // ws.registerPlugin(TimelinePlugin.create())

    // Initialize the Timeline plugin
    // wavesurfer.registerPlugin(TimelinePlugin.create());
    let regionsPlugin = wavesurfer.registerPlugin(WaveSurfer.Regions.create()); // try to access wavesurfer.plugins[0]
    // AJOUTER le addEvent ICI 1 seule fois
    regionsPlugin.on("region-created", () => {
        console.log("region-created event fired !");
        addCloseBtns(regionsPlugin);
    })
    
    wavesurfer.on(
        'interaction', 
        () => {wavesurfer.play()}
    );

    document.querySelector("div#waveform > div").addEventListener(
        "contextmenu",
        (event) => {
            event.preventDefault();
            wavesurfer.playPause();
        }
    );

    // cloning buttons to remove previous eventListeners
    const oldBtnAdd = document.querySelector("button#add-region");
    const newBtnAdd = oldBtnAdd.cloneNode(true);
    oldBtnAdd.parentNode.replaceChild(newBtnAdd, oldBtnAdd);
    newBtnAdd.addEventListener(
        "click",
        () => {
            addRegion(regionsPlugin, 3, 4);
        }
    );
    const oldBtnSave = document.querySelector("button#save-regions");
    const newBtnSave = oldBtnSave.cloneNode(true);
    oldBtnSave.parentNode.replaceChild(newBtnSave, oldBtnSave);
    newBtnSave.addEventListener(
        "click",
        () => {
            saveData(fpath, regionsPlugin);
        }
    );

    wavesurfer.on(
        'destroy', 
        () => {
            wavesurfer.unAll()
        }
    );

    addRegions(notes, regionsPlugin);
    // return false;
}

// var last_region = null;


/**
 * Add regions to the wavesurfer canvas.
 *
 * @param {Object} notes  List of regions to add.
 * @param {WaveSurfer.Regions} regionsP Regions Plugin object.
 * @returns {void}
 */
async function addRegions(data, regionsP){
    if (data.notes){
        for (let note of data.notes) {
            await addRegion(regionsP, note.start, note.end);
        }
    } 
    else {
        displayToast("No data was found for that file.");
    }
}


/**
 * Add one region to the wavesurfer canvas.
 *
 * @param {WaveSurfer.Regions} regionsP Regions Plugin object.
 * @param {number} [start=2]    Starting time of the region to add.
 * @param {number} [end=2.2]    Ending time of the region to add.
 */
async function addRegion(regionsP, start=2, end=2.2){
    // const end = start + 0.2;
    // regionsPlugin = ws.registerPlugin(RegionsPlugin.create());
    const color = randomColor();

    let region = regionsP.addRegion({
        color: color,
        // content?: string | HTMLElement, // text
        drag: true,
        start: start,
        end: end,
        id: color, // l'id apparait dans l'attribut HTML "part"
        // maxLength?: number,
        // minLength?: number,
        resize: true,
    }); // returns a SingleRegion object
}


function addCloseBtns(regionsP){
    try {
        let region = null;
        let waveformRoot = document.querySelector('#waveform > div').shadowRoot;
        let regionDiv = waveformRoot.children[1].querySelector("div.scroll > div.wrapper > div:last-of-type");
        for (let el of regionDiv.children) {
            if (el.getElementsByTagName("button").length == 0){ // détecter si elle ne contient pas un closeBtn
                for (let r of regionsP.getRegions()) { // retrouver la bonne entrée
                    if (r.id === el.part[1]) {
                        region = r;
                    }
                }

                let closeBtn = document.createElement("button");
                closeBtn.style = 'background-color: transparent; border-width: 0px; position: absolute; top: 3px; right: 3px; color: gray; cursor: pointer; z-index: 30;';
                closeBtn.innerHTML = "×";
                closeBtn.addEventListener(
                    "click",
                    (event) => {
                        event.stopPropagation();
                        region.remove();
                    }
                );
                el.appendChild(closeBtn);
            }
        }
    }
    catch (err) {
        console.error(err);
    }
}


function removeRegion(regionsP){
    regionsP.destroy();
    // lister les régions ?
}


/**
 * Generates a random color.
 *
 * @return {String} The random color. 
 */
function randomColor(){
    const random = (min, max) => Math.trunc(Math.random() * (max - min) + min);
    return `rgba(${random(10, 255)},${random(10, 255)},${random(10, 255)},0.5)`;
}


/**
 * Display message in a toast widget. 
 *
 * @param {String} message  Message to display to the user.
 * @returns {void}
 */
async function displayToast(message){
    hideToast();
    const toast = document.getElementById("toast-container");
    toast.querySelector("div.toast-message").innerHTML = message;
    toast.classList.remove("hidden");
    toast.classList.add("absolute");
}


/**
 * Hide the toast widget.
 *
 * @returns {void}
 */
function hideToast(){
    const toast = document.getElementById("toast-container");
    toast.classList.remove("absolute");
    toast.classList.add("hidden");
    toast.querySelector("div.toast-message").innerHTML = "";
}


// Calls
let files = new Array();
// lire chaque fichier avec FileReader puis manipuler avec ArrayBuffer ?
// que faire avec ces fichiers ? lire le son et créer un spectro
console.log("Hello from main.js")

// retirer les modules, juste utiliser plusieurs fichiers sripts