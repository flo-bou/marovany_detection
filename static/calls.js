
/**
 * Prépare une requête GET qui renvoie un json
 * Endpoints available : "/files_list"
 *
 * @param {string} [path=""]
 * @param {string} [params=""]
 * @return {Promise} 
 */
function request_data(path="", params=""){
    let iniObj = {	
        method: 'GET',
        headers: { 
            'Accept': 'application/json',
            'Referer': 'origin'
        },
    };

    let promiseOut = fetch( "http://127.0.0.1:5000"+path+params, iniObj )
    .then( response => {
        console.log("Request of "+path+params);
        if (response.ok){
            return response.json();
        } else{
            console.error(response.status, response.statusText)
        }
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

    return promiseOut;
}


/**
 * Prépare une requête GET qui renvoie du texte
 * Endpoints available : "/", "/test"
 *
 * @param {string} [path=""]
 * @param {string} [params=""]
 * @return {Promise} 
 */
function request_text(path="", params=""){
    let iniObj = {	
        method: 'GET',
        headers: { 
            'Accept': '*/*',
            'Referer': 'origin'
        },
    };

    let promiseOut = fetch( "http://127.0.0.1:5000"+path+params, iniObj )
    .then( response => {
        console.log("Request of "+path+params);
        if (response.ok){
            return response.text();
        } else{
            console.error(response.status, response.statusText)
        }
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

    return promiseOut;
}


/**
 * Prépare une requête GET qui renvoie un blob
 * Endpoints available : "/file?name={{name}}"
 *
 * @param {string} [path=""]
 * @param {string} [params=""]
 * @return {Promise} 
 */
function request_path(path="", params=""){
    let iniObj = {	
        method: 'GET',
        headers: { 
            'Accept': '*/*',
            'Referer': 'origin'
        },
    };

    let promiseOut = fetch( "http://127.0.0.1:5000"+path+params, iniObj )
    .then( response => {
        console.log("Request of "+path+params);
        if (response.ok){
            return response.blob();
        } else{
            console.error(response.status, response.statusText)
        }
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

    return promiseOut;
}

console.log("Hello from calls.js");
