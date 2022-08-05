/**
 * Search validator and regex
 */
import SubParse_ElasticQueryBuilder from "../../../db/elastic_helpers/elastic_query_builder";

class SearchValidator {
    constructor() {

    }

    /**
     * Search string to get matches from
     * 
     * @param {String} value - entry to validate
     * @returns {SubParse_ElasticQueryBuilder} - SubParse_ElasticQueryBuilder
     */
    getmatches(value) {
        let _builder = new SubParse_ElasticQueryBuilder();
        console.log("Search String: " + value);

        const regex = /(?<field>.*?)(?<eval>==|!=)(?<value>.*?)(?<op>&&|\|\||$)/g;
        let _all_matches = [...value.matchAll(regex)];
        let last_match = null;
        console.log(_all_matches);
        console.log(_all_matches.length);
        for (let match of _all_matches) {

            let _full = match[0];
            let _field = match[1].trim();
            let _eval = match[2].trim();
            let _value = match[3].trim();
            let _opt = match[4].trim();
            let _modified = `${_field} ${_eval} ${_value}`;

            if (_opt != "") {
                console.log("There is an OPT To be used");
                // Two cases to handle ( && | || )
                if (_opt == "&&") {
                    console.log("******************");
                    console.log("Using && OPT");
                    console.log("Use modified :: " + _modified);
                    console.log("******************");
                    if (!_builder.addANDValue(_modified)) {
                        this.filterError = true;
                        return null;
                    }
                } else if (_opt == "||") {
                    console.log("******************");
                    console.log("Using || OPT");
                    console.log("Use modified :: " + _modified);
                    console.log("******************");
                    if (!_builder.addORValue(_modified)) {
                        this.filterError = true;
                        return null;
                    }
                } else {
                    console.log("******************");
                    console.log("ERROR WITH ADDING OPT :: WRONG OPT TYPE");
                    console.log("******************");
                }

            } else {
                console.log("NO OPT TO USE :: Try to auto add");

                if (_all_matches.length != 1) {
                    // #region This is for the last item in the search, that has more than 1 item
                    console.log("Trying to add last item");
                    console.log("Prev: " + last_match[4]);
                    if (last_match[4] == "&&") {
                        if (!_builder.addANDValue(_modified)) {
                            this.filterError = true;
                            return null;
                        }
                    } else if (last_match[4] == "||") {
                        if (!_builder.addORValue(_modified)) {
                            this.filterError = true;
                            return null;
                        }
                    } else {
                        console.log("******************");
                        console.log("ERROR WITH ADDING WITHOUT OPT :: LAST OPT, MULTIPLE ITEMS");
                        console.log("******************");
                    }
                } else {
                    // #region This is for either 1 item in the search
                    console.log("Only search param :: Add it");
                    if (_eval == "==") {
                        console.log("Add with :: ==");
                        if (!_builder.addSINGLEValue(_modified)) {
                            this.filterError = true;
                            return null;
                        }
                    } else if (_eval == "!=") {
                        console.log("Add with :: !=");
                        if (!_builder.addSINGLEValue(_modified)) {
                            this.filterError = true;
                            return null;
                        }
                    } else {
                        console.log("******************");
                        console.log("ERROR WITH ADDING WITHOUT OPT :: NO OPT SINGLE ITEM");
                        console.log("******************");
                    }
                    // #endregion

                }
            }
            last_match = match;
        }

        return _builder;
    }

}

const singletonInstance = new SearchValidator();

Object.freeze(singletonInstance);

export default SearchValidator;