
/**
 * Prepares a GET request that returns json data
 *
 * @param {string} [path=""]
 * @param {string} [params=""]
 * @return {Promise|void} 
 */
function request_data(path="", params=""){
    let initObj = {	
        method: 'GET',
        headers: { 
            'Accept': 'application/json',
            'Referer': 'origin'
        },
    };

    const promiseOut = fetch( "http://127.0.0.1:5000"+path+params, initObj )
    .then( response => {
        if (response.ok){
            return response.json();
        } else{
            console.error("Bad response from server during the GET request to : "+path+params);
            console.error(response.status, response.statusText);
        }
    })
    .catch( err => { 
        console.error("An error occured during the GET request to : "+path+params);
        console.error(err);
    })

    return promiseOut;
}


/**
 * Prepares a POST request.
 *
 * @param {string} [path=""]
 * @param {string} [params=""]
 * @return {Promise|void} 
 */
function send_data(path="", data=""){
    const initObj = {	
        method: 'POST',
        headers: { 
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'Referer': 'origin'
        },
        body: data
    };

    const promiseOut = fetch( "http://127.0.0.1:5000"+path, initObj )
    .then( response => {
        if (response.ok){
            return response.text();
        } else{
            console.error("Bad response from server during the POST request to : "+path+params);
            console.error(response.status, response.statusText)
        }
    })
    .catch( err => { 
        console.error("An error occured during the POST request to : "+path+params);
        console.error(err);
    })

    return promiseOut;
}


/**
 * Prepares a GET request that returns a blob
 *
 * @param {string} [path=""]
 * @param {string} [params=""]
 * @return {Promise|void} 
 */
function request_blob(path="", params=""){
    let initObj = {	
        method: 'GET',
        headers: { 
            'Accept': '*/*',
            'Referer': 'origin'
        },
    };

    const promiseOut = fetch( "http://127.0.0.1:5000"+path+params, initObj )
    .then( response => {
        if (response.ok){
            return response.blob();
        } else{
            console.error("Bad response from server during the GET request to : "+path+params);
            console.error(response.status, response.statusText)
        }
    })
    .catch( err => { 
        console.error("An error occured during the GET request to : "+path+params);
        console.error(err);
    })

    return promiseOut;
}

console.log("Hello from calls.js");
