/**
 * User input validator for checking user input in text fields to try avoiding malformed or malicious data from being entered
 */
class InputValidator {
    constructor() { }

    /**
     * Elasticsearch field to validate
     * 
     * @param {String} field - entry to validate
     * @returns {Boolean} - True if field passed validation otherwise False
     */
    validateField(field) {
        return /^[a-zA-Z_.0-9]+$/.exec(field) == null ? false : true;
    }

    /**
     * User or Generated value to validate
     * 
     * @param {String} value - entry to validate
     * @returns {Boolean} - True if field passed validation otherwise False
     */
    validateValue(value) {
        return /^[a-zA-Z-_,.0-9 /=()+]+$/.exec(value) == null ? false : true;
    }


    validate(value) {
        return /^[a-zA-Z-_,.0-9[\]'" /=!&\|()+]+$/.exec(value) == null ? false : true;
    }
}

const singletonInstance = new InputValidator();

Object.freeze(singletonInstance);

export default InputValidator;
