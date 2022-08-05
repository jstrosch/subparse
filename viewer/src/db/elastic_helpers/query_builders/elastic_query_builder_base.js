/**
 * Abstract SubParse Elastic Query Builder Base.
 *
 * @class SubParse_ElasticQueryBuilder
 */
class SubParse_ElasticQueryBuilderBase {
    constructor() {
        if(this.constructor == SubParse_ElasticQueryBuilderBase){
            throw new Error("Abstract classes can't be instantiated");
        }
    }
    
    equalTo(){ 
        throw new Error("Method 'equalTo(field, value)' must be implemented");
    }

    notEqualTo() {
        throw new Error("Method 'notEqualTo(field, value)' must be implemented");
    }

    lessThan() {
        throw new Error("Method 'lessThan(field, value)' must be implemented");
    }

    lessThanOrEqualTo() {
        throw new Error("Method 'lessThanOrEqualTo(field, value)' must be implemented");
    }

    greaterThan() {
        throw new Error("Method 'greaterThan(field, value)' must be implemented");
    }

    greaterThanOrEqualTo() {
        throw new Error("Method 'greaterThanOrEqualTo(field, value)' must be implemented");
    }

    and() {
        throw new Error("Method 'and(value1, value2)' must be implemented");
    }

    or() {
        throw new Error("Method 'or(value1, value2)' must be implemented");
    }
}

export default SubParse_ElasticQueryBuilderBase;