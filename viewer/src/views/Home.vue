<template>
  <div>
    <Search
      ref="searchbarParent"
      @search_event="search_button_clicked"
      @search_reset_event="clear_button_clicked"
      @added_from_suggestion="added_from_suggestion"
      :searchQuery.sync="query"
      :th_results="th_results"
    />
    <!-- #region Loading Pages -->
    <div v-if="table_data.length == 0" style="width: 50%; margin: auto">
      <b-container class="mt-5" align="center">
        <div v-if="showLoading == true" class="h1 mb-0">
          <SemipolarSpinner
            :animation-duration="1200"
            :size="55"
            color="#ff1d5e"
          />
          <br />
          <br />
          <b-card-text class="text-danger">Loading...</b-card-text>
        </div>
        <div v-if="showLoading == false" class="h1 mb-0">
          <SemipolarSpinner
            :animation-duration="1200"
            :size="55"
            color="#ff1d5e"
          />
          <br />
          <br />
          <b-card-text class="text-danger" v-if="table_data.length == 0"
            >No Results From Query</b-card-text
          >
        </div>
      </b-container>
    </div>
    <!-- #endregion End Of Loading Pages -->

    <!-- #region Pagination -->
    <div v-if="table_data.length != 0 && showLoading == false" class="flex table_size_controller">
      <b-form-select class="form-control page-select custom-select" v-model="perPage" :options="options"/>

      <b-pagination 
        aria-controls="data-table"
        v-model="currentPage" 
        :total-rows="table_data.length"
        :per-page="perPage"
      />
      <div class="pagination-info">
          Showing {{ ((perPage * currentPage)-perPage)+1 }} - {{ (perPage * currentPage) > table_data.length ? table_data.length :  (perPage * currentPage) }} of {{ table_data.length }} entries 
      </div>
    </div>
    <!-- #endregion Pagination -->

    <!-- #region Main Table -->
    <div v-if="table_data.length != 0 && showLoading == false">
      <MainDynamicDataTable
        v-if="table_data"
        v-on:add_filter="filterAdded"
        :field_data="field_data"
        :table_data="table_data"
        :currentPage="currentPage"
        :perPage="perPage"
      />
    </div>
    <!-- #endregion Main Table -->
  </div>
</template>

<script>
import SearchValidator from "./utils/validators/SearchValidator";
import MainDynamicDataTable from "./dynamic_views/MainDynamicDataTable.vue";
import SubParse_ElasticQueryBuilder from "../db/elastic_helpers/elastic_query_builder.js";
import SubParse_ElasticClient from "../db/elastic_client.js";
import Search from "./search/Search.vue";
import { SemipolarSpinner } from "epic-spinners";

export default {
  data: function () {
    return {
      perPage: 10,
      currentPage: 1,
      rows: 0,
      options: [
        {
            "value": 10,
            "text": "10 per page"
        },
        {
            "value": 50,
            "text": "50 per page"
        },
        {
            "value": 100,
            "text": "100 per page"
        },
        {
            "value": 200,
            "text": "200 per page"
        },
        {
            "value": 500,
            "text": "500 per page"
        },
        {
            "value": 1000,
            "text": "1000 per page"
        }
      ],
      field_data: [
        {
          key: "details",
          label: "Details",
          thStyle: { width: "5%" },
        },
        {
          key: "file_name",
          label: "File Name",
          thStyle: { width: "20%" },
          sortable: true,
        },
        {
          key: "file_magic",
          label: "File Magic",
          thStyle: { width: "20%" },
          sortable: true,
        },
        {
          key: "file_size",
          label: "File Size",
          thStyle: { width: "10%" },
          sortable: true,
        },
        {
          key: "file_extension",
          label: "Orig. Extension",
          thStyle: { width: "10%" },
          sortable: true,
        },
        {
          key: "derived_extension",
          label: "Derivded Extension",
          thStyle: { width: "10%" },
          sortable: true,
        },
        {
          key: "used_enrichers",
          label: "Enrichers",
          thStyle: { width: "20%" },
          sortable: true,
        },
        {
          key: "added_on",
          label: "Added",
          thStyle: { width: "20%" },
          sortable: true,
        },
      ],
      table_data: [],
      query: "",
      wasUpdated: undefined,
      value: "",
      showLoading: true,
      operations: ["==", "!=", "<", "<=", ">", ">="],
      types: ["&&", "||"],
      th_results: [],
      typeahead_data: [],
      th_suggestions: {},
    };
  },
  components: {
    MainDynamicDataTable,
    Search,
    SemipolarSpinner,
  },
  watch: {
    query: function () {
      try {
        var _splitQueryOrig = this.splitExpression(this.query);
        var _splitQuery = _splitQueryOrig.at(-1);
        if(_splitQuery !== undefined){
          if(this.operations.includes(_splitQuery) || this.operations.includes(_splitQueryOrig.at(-2))){
            if(this.operations.includes(_splitQuery)) {
              SubParse_ElasticClient.search.getValueDataForFields(_splitQueryOrig.at(-2)).then((_) => { 
                this.th_results = _;
              });
            }else if(this.operations.includes(_splitQueryOrig.at(-2))) {
              SubParse_ElasticClient.search.getValueDataForFields(_splitQueryOrig.at(-3)).then((_) => { 
                var _r = new RegExp(_splitQuery);
                var _p_results = _.filter((item) =>
                  _r.test(item)
                );
                if(_p_results.length == 1){
                  if(_p_results.at(0) == _splitQuery){
                    _p_results = [];
                  }
                }

                this.th_results = _p_results;
              }); 
            }
          }
          else if(_splitQueryOrig.length > 2 && this.operations.includes(_splitQueryOrig.at(-2))) {
            this.th_results = [];
          }else{
            if ((_splitQuery.includes("=") || _splitQuery.includes("!")) && !_splitQuery.includes("==") && !_splitQuery.includes("!=")) {
              this.th_results = ["==", "!="];
            } else if (_splitQuery.includes("&") && !_splitQuery.includes("&&")) {
              this.th_results = ["&&"];
            } else if (_splitQuery.includes("|") && !_splitQuery.includes("||")) {
              this.th_results = ["||"];
            } else {
              var _reg = new RegExp(_splitQuery);
              var _pending_results = this.typeahead_data.filter((item) =>
                _reg.test(item)
              );

              if(_pending_results.length == 1){
                if(_pending_results.at(0) == _splitQuery){
                  _pending_results = [];
                }
              }
              this.th_results = _pending_results;
            }
          }
        }else{
          this.th_results = [];
        }
      } catch (e) {
        console.log("Query is undefined");
        console.log(e);
        this.th_results = [];
      }
    },
  },
  methods: {
    added_from_suggestion: function (val) {
      var _split = this.splitExpression(this.query);

      if(val.includes(_split.at(-1))){
        _split.splice(-1, 1, val);
      }else{
        _split.push(val);
      }
      
      this.query = _split.join(" ");  
      this.th_results = [];
      this.$refs.searchbarParent.$refs.searchbar.$el.focus();
    },
    filterAdded(filter, operator) {
      if (this.query.length != 0) {
        this.query += " " + operator + " ";
      }

      this.query += filter;
    },
    async getTypeaHeadData() {
      var _client = SubParse_ElasticClient;
      var _notProcssesedTHData = await _client.search.getCleanedFields();

      this.typeahead_data = this.keyify(_notProcssesedTHData);
    },
    async getTableData() {
      const body = {
        size: 200,
        from: 0,
      };
      this.table_data = await SubParse_ElasticClient.search.getDocuments(body);
      this.showLoading = false;
    },
    async getTableDataWithBuilder(builder) {
      this.table_data = await SubParse_ElasticClient.search.queryWithBuilder(
        builder
      );
      this.showLoading = false;
    },
    addSeachParam(params) {
      params["orig_string"] = this.query;
      history.pushState(
        {},
        null,
        this.$route.path +
          "?search=" +
          btoa(encodeURIComponent(JSON.stringify(params)))
      );
    },
    search_button_clicked() {
      var builder = this.parseQuery(this.query);
      if (builder != null) {
        SubParse_ElasticClient.search.queryWithBuilder(builder).then((data) => {
          this.table_data = data;
        });
        this.addSeachParam(builder);
      }
    },
    parseQuery: function (str) {
      return new SearchValidator().getmatches(str);
    },
    clear_button_clicked() {
      this.query = "";
      this.getTableData();
      history.pushState({}, null, this.$route.path);
    },
    keyify: function (obj, prefix = "") {
      // does the heavy lifting for generating the typeahead suggestions for 'preprocessing'
      return Object.keys(obj).reduce((res, el) => {
        if (typeof obj[el] === "object" && obj[el] !== null) {
          if(JSON.stringify(obj[el]) === '{}'){
            return [...res, prefix + el];
          }else if(!Object.prototype.hasOwnProperty.call(obj[el],"fields") && !Object.prototype.hasOwnProperty.call(obj[el],"type")){
            return [...res, ...this.keyify(obj[el], prefix + el + ".")];
          }
          else{
            return [...res, prefix + el];
          }
        }
        return [...res, prefix + el];
      }, []);
    },
    /**
     * Splits a string into tokens
     * @param {string} input The string to be tokenized
     */
    splitExpression: function (input) {
      // replace spaces that are not enclosed in quotes
      input = input.replace(/ (?=([^"]*"[^"]*")*[^"]*$)/g, "");

      const output = [];
      let cur = "";

      for (let i = 0, ilen = input.length; i < ilen; i++) {
        if (/[)(]/.test(input[i])) {
          if (cur !== "") {
            output.push(cur);
          }
          output.push(input[i]);
          cur = "";
        } else if (cur === "") {
          cur += input[i];
        } else if (
          /[!&|=<>]/.test(cur) ||
          cur === "EXISTS" ||
          cur === "EXISTS!"
        ) {
          if (
            (/[&|=<>]/.test(input[i]) && cur !== "EXISTS!") ||
            (cur === "EXISTS" && input[i] === "!")
          ) {
            cur += input[i];
          } else {
            output.push(cur);
            cur = input[i];
          }
        } else if (/[!&|=<>]/.test(input[i])) {
          output.push(cur);
          cur = input[i];
        } else {
          cur += input[i];
        }
      }

      if (cur !== "") {
        output.push(cur);
      }
      // console.log("From split expression: ");
      // console.log(output);
      return output;
    },
  },
  mounted: function() {
    this.$nextTick(() => {
        var _hasSearch = new URL(location.href).searchParams.get("search");
        if (_hasSearch != null) {
          var _data = JSON.parse(decodeURIComponent(atob(_hasSearch)));
          // console.log("Json decoded: " + JSON.stringify(_data));
          var _builderData = new SubParse_ElasticQueryBuilder();
          _builderData.fromJSON(_data);

          this.query = _data["orig_string"];

          try {
            this.getTableDataWithBuilder(_builderData);
          } catch (e) {
            console.log("Error with query passed");
          }
        } else {
          this.getTableData();
        }

        this.getTypeaHeadData();
      }
    );
  }
};
</script>

<style scoped>
  .pagination {
    justify-content: center;
    text-align: center;
    margin-bottom: 0px;
    padding-top: 10px;
    padding-bottom: 10px;
  }
  #page_size_selector {
    margin-top: 10px;
  }

  .flex {
    display: flex;
  }
  .form-control {
    width: auto;
    padding: 0rem 0rem;
    margin-top: 10px;
    margin-bottom: 10px;
  }
  .pagination-info {

    border: 1px solid #9E9E9E;
    border-radius: 0 0.25rem 0.25rem 0;
    color: #f5f5f5;
    display: inline-block;
    text-align: center;
    font-size: .8rem;
    /* margin-left: -6px; */
    padding: 5px 5px;
    margin-top: 10px;
    margin-bottom: 10px;
  }

  .table_size_controller {
    padding-left: 10px;
  }
</style>