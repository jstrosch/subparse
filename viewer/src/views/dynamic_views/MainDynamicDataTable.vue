<template>
  <div>  
    <b-table 
      id="data-table" 
      :per-page="perPage"
      :current-page="currentPage"
      :items="table_data" 
      :fields="field_data" 
      head-variant 
      responsive 
      striped 
      hover 
      fixed>

      <template #cell(added_on)="row">
        <p>{{ converttime(row.item.added_on) }}</p>
      </template>

      <template #cell(file_magic)="row">
        <p>{{ row.item.file_magic.slice(0, 30) }}...</p>
      </template>
      
      <template #cell(abuse_signature)="row">
        <p>{{ row.item.abuse_signature }}</p>
      </template>

      <template #cell(file_size)="row">
        <p>{{ convertbytes(row.item.file_size) }}</p>
      </template>

      <template #cell(used_enrichers)="row">
        <p v-for="(enricher, key) in row.item.used_enrichers" :key="key">
          {{enricher}}
        </p>
        <!-- <p>{{ cleanArray(row.item.used_enrichers) }}</p> -->
      </template>

      <template #cell(derived_extension)="row">
        <p>{{ row.item.derived_extension }}</p>
      </template>

      <template #cell(details)="row">
        <b-button v-if="row.detailsShowing" size="sm" @click="row.toggleDetails" variant="outline-dark">
          <b-icon icon="arrow-up"/>  
        </b-button>
        <b-button v-else size="sm" @click="row.toggleDetails" variant="outline-dark">
          <b-icon icon="plus"/>
        </b-button>
      </template>

      <template #row-details="row">
        <!-- #region Dynamic Details -->
        <b-card>
            <GeneralInfoRow v-on="$listeners" :item="row.item"/>
            <DynamicParserRow  v-on="$listeners" :item="row.item" :supportedComponents="row.item.used_parsers"/>
            <DynamicEnricherRow  v-on="$listeners" :item="row.item" :supportedComponents="row.item.used_enrichers"/>
        </b-card>
        <!-- #endregion -->
      </template>
      
    </b-table>
  </div>
</template>

<script>
  import DynamicParserRow from "./dynamic_row/DynamicParserRow.vue";
  import DynamicEnricherRow from "./dynamic_row/DynamicEnricherRow.vue";
  import GeneralInfoRow from "./dynamic_row/GeneralInfoRow.vue";
  import * as Helpers from "../utils/helpers/Helpers";;
  export default {
    name: "MainDynamicDataTable", 
    components: {
      DynamicParserRow,
      DynamicEnricherRow,
      GeneralInfoRow
    },
    props:  {
      /**
       * Data to be used for the table body
       */
      table_data: {
          type: Array,
          required: true,
      },
      /**
       * Column header information
       */
      field_data: {
          type: Array,
          required: true,
      },
      perPage: {
        type: Number,
        default: 14,
        required: false
      },
      currentPage: {
        type: Number,
        required: true
      }
    },
    computed: {
      rows() {
        return this.table_data.length
      }
    },
    methods: {
      ...Helpers
    }
  }
</script>
