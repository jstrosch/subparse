'use strict';
import SubParse_ElasticClient_Base from './elastic_helpers/client_base/elastic_client_base.js';
import SubParse_ElasticSearch from './elastic_helpers/elastic_search.js';

class SubParse_ElasticClient extends SubParse_ElasticClient_Base { 
    /**
     * Constructor 
     * 
     * @param {*} host - host for the Elasticsearch instance/cluster
     */
    constructor(host) {
        super(host);
        this.search = new SubParse_ElasticSearch(this.client);
        this.search_fields = this.search.getCleanedFields();
    }
}

const singletonInstance = new SubParse_ElasticClient("http://localhost:9200");

Object.freeze(singletonInstance);

export default singletonInstance