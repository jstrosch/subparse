import SubParse_ElasticQueryBuilderBase from "./query_builders/elastic_query_builder_base.js";
import InputValidator from "../../views/utils/validators/InputValidator";

/**
 * SubParse Elastic Query Builder is used to create the dictionary/json that is used for quering the Elasticsearch instance or cluster
 *  this allows for standarization and simplifies changes to the query generation. 
 * 
 * @class SubParse_ElasticQueryBuilder
 * @implements SubParse_ElasticQueryBuilderBase
 * 
 */
class SubParse_ElasticQueryBuilder extends SubParse_ElasticQueryBuilderBase {
    constructor() {
        super();
        this.should = []; // OR
        this.should_not = []; // NOR

        this.must = []; // AND
        this.must_not = [];
    }

    /**
     * 
     * @param {String} value Full query string to be used: field (!= | ==) value 
     * @returns {Boolean} True/False if added or not
     */
    addANDValue(value) {
        if (new InputValidator().validate(value)) {
            if (String(value).includes(' == ')) {
                return this.equalTo(value, false);
            } else if (String(value).includes(' != ')) {
                return this.notEqualTo(value, false);
            } else {
                return false;
            }
        } else {
            return false;
        }
    }

    /**
     * 
     * @param {String} value Full query string to be used: field (!= | ==) value  
     * @returns {Boolean} True/False if added or not
     */
    addORValue(value) {
        if (new InputValidator().validate(value)) {
            if (String(value).includes(' == ')) {
                return this.equalTo(value, true);
            } else if (String(value).includes(' != ')) {
                return this.notEqualTo(value, true);
            } else {
                return false;
            }
        } else {
            return false;
        }
    }

    /**
     * 
     * @param {String} value Full query string to be used: field (!= | ==) value  
     * @returns {Boolean} True/False if added or not
     */
    addSINGLEValue(value) {
        // console.log(new InputValidator().validate(value));
        if (new InputValidator().validate(value)) {
            if (String(value).includes(' == ')) {
                return this.equalTo(value, false);
            } else if (String(value).includes(' != ')) {
                return this.notEqualTo(value, false);
            } else {
                return false;
            }
        } else {
            return false;
        }
    }

    /**
     * Adds a value that is meant for the field == value query
     * 
     * @param {String} value - value that should be added to the query
     * @param {Boolean} should_must - if the value is being added from an OR event or not (should: true, must: false)
     * @returns {Boolean} - True is added with no issue, False if was not able to be added
     */
    equalTo(value, should_must) {
        let _fieldValue = String(value).split("==");
        let _field = _fieldValue[0].trim();
        let _value = _fieldValue[1].trim();

        console.log(value);

        let _tmp = { "match_phrase": {} };
        _tmp["match_phrase"][_field] = _value;

        if (should_must) {
            this.should.push(_tmp);
        } else {
            this.must.push(_tmp);
        }
        return true;
    }

    /**
     * Adds a value that is meant for the field != value query
     * 
     * @param {String} value - value that should be added to the query
     * @param {Boolean} should - if the value is being added from an OR event or not
     */
    notEqualTo(value, should) {
        console.log("Working overload != ", value);
        let _fieldValue = String(value).split("!=");
        let _field = _fieldValue[0].trim();
        let _value = _fieldValue[1].trim();
        let _section = undefined;

        if (should) {
            _section = this.should_not;
        } else {
            _section = this.must_not;
        }

        let _tmp = {
            "bool": {
                "filter": [

                ]
            }
        };

        let _tmp1 = {
            "match_phrase": {}
        };

        _tmp1['match_phrase'][_field] = _value;
        _tmp['bool']['filter'].push(_tmp1);

        console.log("_tmp " + _tmp);
        _section.push(_tmp);
        return true
    }

    /**
     * Generate dictionary for the query that is needed for the POST to Elasticsearch
     * 
     * @returns {Dictionary} - generated query
     */
    getQuery() {

        let _data = {
            "query": {
                "bool": {

                }
            }
        };

        if (this.should.length != 0) {
            _data['query']['bool']['should'] = this.should;
        }

        if (this.should_not != 0) {
            _data['query']['bool']['should'] == this.should_not;
        }

        if (this.must_not.length != 0) {
            _data['query']['bool']['must_not'] = this.must_not;
        }

        if (Object.keys(this.must).length != 0) {
            _data['query']['bool']['must'] = this.must;
        }

        console.log("Query data: ", _data);
        return _data;
    }

    /**
     * 
     * @param {Dictionary} json_data - data from previous query
     */
    fromJSON(json_data) {
        this.should = json_data.should;
        this.should_not = json_data.should_not;
        this.must = json_data.must;
        this.must_not = json_data.must_not;
    }
}

export default SubParse_ElasticQueryBuilder;