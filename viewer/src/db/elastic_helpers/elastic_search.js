import SubParse_Doc from './base/subparse_document';
import axios from 'axios';

/**
 * Main object that is used for generation of the Elasticsearch Search Query
 */
class SubParse_ElasticSearch {
    /**
     * Constructor
     * 
     * @param {SubParse_ElasticClient_Base.client} client - Client Object for communicating with Elasticsearch
     */
    constructor(client) {
        if (typeof client === "object") {
            this.client = client;
        } else {
            throw Error("SubParse_ElasticClient Error");
        }
    }

    /**
     * Query the Elasticsearch client for a document
     * 
     * @param {Dictionary} body - body to be used for the POST request to the Elasticsearch instance
     * @returns {list} - empty list if no results from query were found or the cleaned results from the query 
     */
    #query_document(body) {
        console.log("Query for elastic: ", body);
        body['size'] = 10000;

        return this.client.search({ index: "files", body: body })
            .then((results) => {
                let _cleaned = [];
                results.hits.hits.forEach((hit) => {
                    let _obj = new SubParse_Doc(hit);
                    _cleaned.push(_obj);
                });
                return _cleaned;
            })
            .catch((err) => {
                console.log(err);
                return [];
            });
    }
    /**
     * Query the Elasticsearch client using the builder to generated the needed query object
     * 
     * @param {SubParse_ElasticQueryBuilder.builder} - builder to be used to create the body for the POST request
     * @returns {list} - empty list if no results from query were found or the cleaned results from the query 
     */
    queryWithBuilder(builder) {
        const body = {
            query: builder.getQuery()['query']
        };

        body['size'] = 10000;

        // Simple POST request with a JSON body using axios
        return this.client.search({ index: "files", body: body, size: 10000 })
            .then((results) => {
                let _cleaned = [];

                results.hits.hits.forEach((hit) => {
                    let _obj = new SubParse_Doc(hit);
                    _cleaned.push(_obj);
                });
                return _cleaned;
            })
            .catch((err) => {
                console.log(err);
                return [];
            });
    }


    isObject = (value) => {
        return !!(value && typeof value === "object" && !Array.isArray(value));
    };

    _remove_properties(data, ndata) {
        // console.log(Object.keys(data));
        if (this.isObject(data)) {
            Object.keys(data).forEach(k => {
                if (Object.keys(data[k]).includes("properties")) {
                    ndata[k] = {};
                    this._remove_properties(data[k]['properties'], ndata[k]);
                } else {
                    ndata[k] = data[k];
                }
            });
        }
    }

    //#region Mapping Cleaner
    /**
     * Removes the nested 'properties' from the JSON Data.
     * This needs to be changed to using recursion to complete this.
     * Works for now just brittle with the data being collected and tied to the current field levels
     * 
     * @param {Dictionary} data - data from Elasticsearch that needs to be cleaned
     * @returns {Dictionary} - cleaned Elasticsearch data that is ready for use
     */
    $_cleanMappingData(data) {
        let _newData = {};
        this._remove_properties(data, _newData);
        return _newData;
    }
    //#endregion 

    /**
     * Used to get the needed mapping data for typeahead abilities
     * URL: localhost:9200/files,files/_mapping?pretty
     * 
     * @returns {list} - cleaned pretty mapping results
     */
    getCleanedFields() {
        return new Promise((resolve, reject) => {
            const options = {
                url: 'http://localhost:9200/files,files/_mapping?pretty',
                method: 'GET'
            };

            axios(options)
                .then((response) => {
                    resolve(this.$_cleanMappingData(response.data.files.mappings.properties));
                }, (error) => {
                    reject(error);
                });
        });
    }

    /**
     * Query Elasticsearch for the possible values for a field.
     * 
     * @param {String} field - field to be used as the 'keyword' for typeahead quering
     * @returns {list} - cleaned list of the current options for typeahead results
     */
    getValueDataForFields(field) {
        return new Promise((resolve, reject) => {
            let options = {
                "aggs": {
                    "rdata": {
                        "terms": {
                            "field": field + ".keyword"
                        }
                    }
                },
                "size": 0
            }
            axios.get('http://localhost:9200/files/_search?pretty', {
                params: {
                    source: JSON.stringify(options),
                    source_content_type: 'application/json'
                }
            }).then((response) => {
                resolve(this._cleanValueDataForTH(response.data.aggregations.rdata.buckets));
            }, (error) => {
                reject(error);
            });
        });
    }

    /**
     * Clean dictionary data to get it ready for usage with the typeahead implementation
     * 
     * @param {dictionary} data - results to clean from Elasticsearch query for typeahead result list
     * @returns {list} - cleaned list of the typeahead results
     */
    _cleanValueDataForTH(data) {
        if (data.length != 0) {
            let _ = [];
            data.forEach((item) => {
                _.push(item['key']);
            });
            return _;
        } else {
            return [];
        }
    }

    /**
     * Query Elasticsearch for a given document ID
     * 
     * @param {String} doc_id - document id to query for
     * @returns {list} - a empty list if nothing or a list with the document
     */
    getDocByID(doc_id) {
        const body = {
            size: 10000,
            from: 0,
            query: {
                match: {
                    _id: doc_id,
                },
            },
        };

        return this.#query_document(body);
    }

    /**
     * Query Elasticsearch for a set of documents
     * 
     * @param {Dictionary} query - dictionary query that will be used as the POST body to Elasticsearch
     * @returns {list} - a empty list if nothing or a list with the document
     */
    getDocuments(query) {
        return this.#query_document(query);
    }

    /**
     * Query Elasticsearch and get the document ids that were found in the query
     * 
     * @param {Dictionary} query - dictionary query that will be used as the POST body to Elasticsearch
     * @returns {list} - a empty list if nothing or a list with the document
     */
    getSearchedDataIDs(query) {
        const body = {
            size: 10000,
            from: 0,
            query: {
                query_string: {
                    query: query
                }
            }
        };

        return this.client
            .search({ index: "files", body: body })
            .then((results) => {
                let _doc_ids = [];
                results.hits.hits.forEach((hit) => {
                    _doc_ids.push(hit._id);
                });
                return _doc_ids;
            }).catch((err) => {
                console.log(err);
                return [];
            });

    }
}

export default SubParse_ElasticSearch;