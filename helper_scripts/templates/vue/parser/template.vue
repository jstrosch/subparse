<template>
  <div> 
      <b-card bg-variant="subparse-default" text-variant="white" header="String Enricher" no-body>    
          <!-- #region String Output start -->
          <br/>    
          <!-- Show something to the user here : Below an example of using the Filter Table -->
          <!-- <div v-for="(type, key) in item" :key="key">
              <div v-if="type.length != 0">
                  <p class="card-header">{{strings_dir_match[key]}}</p>
                  <FilterTable v-if="type.length != 0" v-on="$listeners" :items="cleanList(type, key)" :fields="[key]" leading="SUBFILTER.enricher_data.STRINGEnricher."/>
                  <br/>
              </div>
          </div> -->
          <!-- #endregion String Output end -->
      </b-card>
  </div>
</template>

<script>
import FilterTable from "../utils/filterTable/FilterTable.vue";
import FilterDropDownMenu from "../utils/dropdown/FilterDropDownMenu.vue";
import * as Helpers from "../utils/helpers/Helpers";

export default {
  name: "templateparser_view",
  data: function () {
    return {};
  },
  components: {
    FilterTable,
    FilterDropDownMenu,
  },
  props: {
    /**
     * Data to be ingested in the template
     */
    item: {
      type: Object,
      required: true,
    },
  },
  methods: {
    ...Helpers
  },
};
</script>