
let ESC = require("elasticsearch");
/**
 * Base class for the SubParser Elasticsearch Client. This allows for the connection and checking to make sure the instance/cluster is available
 * 
 * @class SubParse_ElasticClient_Base
 */
class SubParse_ElasticClient_Base { 
    /**
     * Constructor
     * 
     * @param {*} host - host for Elasticsearch Connection
     */
    constructor(host) { 
        try{
            this.client = ESC.Client({ host: host});
            if(this.#ping()){
                console.log("Elastic connection established");
            }

        }catch{
            console.log("Error connecting to elastic db");
        }
    }

    /**
     * Used for making sure that the Elastic instance/cluster is live and available for connection
     */
    #ping() { 
        console.log("Checking connection to elastic");
        this.client.ping(
            {
                requestTimeout: 30000,
            },
            function (error) {
                if (error) {
                    throw error;
                } else {
                    return true;
                }
            }
        );
    }
}

export default SubParse_ElasticClient_Base;