/**
 * SubParser Elasticsearch Document representation
 * 
 * @class SubParse_Doc
 */
class SubParse_Doc { 
    /**
     * Constructor
     * 
     * @param {Dictionary} data - dictionary/json from Elasticsearch
     */
    constructor(data) { 
        this.md5 = data?._source?.md5;
        this.md5_short = data?._source?.md5?.substring(0,15) + "...";
        
        this.parser_type = data?._source?.parser_type;
        this.file_magic = data?._source?.file_magic;
        this.file_extension = data?._source?.file_extension;
        this.derived_extension = data?._source?.derived_extension;

        this.used_parsers = data?._source?.used_parsers;
        this.used_enrichers = data?._source?.used_enrichers;

        this.enricher_data = data?._source?.enricher_data;
        this.parser_data = data?._source?.parser_data;

        this.file_name = data?._source?.file_name.substring(0,15) + "...";
        this.file_size = data?._source?.file_size
        this.added_on = data?._source?.added_on
        this.updated_on = data?._source?.updated_on

        this.isActive = false;
        this._showDetails = false;
    }
}

export default SubParse_Doc;