/*
* Helper functions that have been needed when working with data to get it ready for display
*/

/**
 * Returns keys from a given dictionary
 * 
 * @param {Object} dict
 * @returns {string[]} string array of keys
 */
function getKeys(dict) {
    return Object.keys(dict);
}

/**
 * Get the keys from an array of dictionaries
 * 
 * @param {Array} arry 
 * @returns {string[]} string array of keys
 */
function getKeyFromList(arry) {
    var _ = [];
    arry.forEach((element) => {
        var _keys = Object.keys(element);
        _keys.forEach((k) => {
            if (!_.includes(k)) {
                _.push(k);
            }
        });
    });
    return _;
}

/** 
 * Clean the imports and get them reasy to be used since they are nested
 */
function getCleanImports(array) {
    var _cleaned = {};

    array.forEach((dict1) => {
        var _k = getKeys(dict1);

        _k.forEach((_k1) => {
            _cleaned[_k1] = [];
            var _elm = {};

            dict1[_k1].forEach((_k2) => {
                var _keys = Object.keys(_k2);
                _keys.forEach((_kf) => {
                    if (!(_kf in _elm)) {
                        _elm[_kf] = _k2[_kf];
                    }
                });
            });
            _cleaned[_k1].push(_elm);
        });
    });
    return _cleaned;
}

/** 
 * Get the keys for the nested imports 
 */
function getKeysNoneNull(dict) {
    var _ = [];
    Object.keys(dict).forEach((key) => {
        if (dict[key] != null) {
            _.push(key)
        }
    });
    return _;
}

function containsKey(obj, key) {
    return Object.keys(obj).includes(key);
}


/**
 * Converts raw bytes into a more readable format
 */
function convertbytes(bytes, decimals = 2) {
    if (bytes === 0) return '0 Bytes';

    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];

    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

/**
 * Converts time stamp into a easier to read format
 */
function converttime(datetime) {
    const current = new Date(datetime);
    const date = (current.getMonth() + 1) + '/' + current.getDate() + '/' + current.getFullYear();
    const time = ('0' + current.getHours()).slice(-2) + ":" + ('0' + current.getMinutes()).slice(-2) + ":" + ('0' + current.getSeconds()).slice(-2);
    const dateTime = date + ' ' + time;
    return dateTime;
}

/**
 * Clean enricher data for displaying
 */
function cleanArray(arry) {
    let cleaned = "";
    if (arry.length != 0) {
        let current = 0;
        for (const element of arry) {
            cleaned += element
            current += 1;
            if (current != arry.length) {
                cleaned += ",";
            }
        }
    } else {
        cleaned = "N/A";
    }
    return cleaned;
}

/**
* Get the keys to be used for the filter table 
*/
function cleanList(arry, header_name) {
    let _ = [];
    arry.forEach((element) => {
        let _tmp = {};
        _tmp[header_name] = element;
        _.push(_tmp);
    });
    console.log(_);
    return _;
}

export {
    getKeys,
    getKeyFromList,
    getCleanImports,
    getKeysNoneNull,
    containsKey,
    convertbytes,
    converttime,
    cleanArray,
    cleanList
};