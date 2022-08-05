<template>
  <div>  
    <b-table thead-class="text-white" class="perow" :items="items" :fields="fields" 
      head-variant responsive striped hover>
      <template v-slot:[`cell(${b})`]="data" v-for="(b, index) in fields">
        <FilterDropDownMenu v-if="data.item[b] && searchInList" v-on="$listeners" :value="data.item[b]" :dbpath="isListDBPath(leading, b)" :key="index + 't'"/>
        <FilterDropDownMenu v-if="data.item[b] && !searchInList" v-on="$listeners" :value="data.item[b]" :dbpath="leading + b" :key="index + 'f'"/>
      </template> 
    </b-table>
  </div>
</template>

<script>

import FilterDropDownMenu from '../dropdown/FilterDropDownMenu.vue';

export default {
    name: "FilterTable",
    components: {
      FilterDropDownMenu
    },
    methods: {
      isListDBPath: function(leading, key) {
        return leading + "." + key;
      }
    },
    props: {
      /**
       * Array of dictionary items to be used for generating the table
       */
      items: {
        type: Array,
        required: true
      },
      /**
       * Array of Strings to be used for the column headers
       */
      fields: {
        type: [String, Array],
        required: true
      },
      /**
       * Leading path before the Database Path, for finding the field(s) in Elasticsearch
       */
      leading: {
        type: String,
        default: "",
        required: false
      },
      /**
       * This needs to be set to True for if the data that needs to be searched on is within a list.
       * Ex: program_headers.gnu_versions.symbols.index.['index'] == value
       */
      searchInList: {
        type: Boolean,
        required: false,
        default: false
      }
    }
}
</script>