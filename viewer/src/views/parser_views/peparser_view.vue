<template>
  <div>
    <b-card
      bg-variant="subparse-default"
      text-variant="white"
      header="PE Parser"
      no-body
    >
      <!-- #region General Information Start -->
      <br />
      <table class="general">
        <tbody>
          <tr>
            <td width="50%">
              <FilterDropDownMenu
                :field="'PE Signature'"
                :value="item.pe_signature"
                :displayFieldName="true"
                v-on="$listeners"
                :dbpath="'parser_data.PEParser.pe_signature'"
              />
            </td>
            <td width="50%">
              <strong>PE Section Count: </strong>{{ item.sections.length }}
            </td>
          </tr>

          <tr>
            <td width="50%">
              <strong>PE File Version: </strong>{{ item.file_version }}
            </td>
          </tr>
          <br />
          <tr>
            <td width="50%">
              <FilterDropDownMenu
                :field="'Image Base'"
                :value="item.image_base"
                :displayFieldName="true"
                v-on="$listeners"
                :dbpath="'parser_data.PEParser.image_base'"
              />
            </td>
            <td width="50%">
              <FilterDropDownMenu
                :field="'Entry Address'"
                :value="item.entry_point"
                :displayFieldName="true"
                v-on="$listeners"
                :dbpath="'parser_data.PEParser.entry_point'"
              />
            </td>
          </tr>

          <tr>
            <td width="50%">
              <FilterDropDownMenu
                :field="'Import Count'"
                :value="item.total_imports"
                :displayFieldName="true"
                v-on="$listeners"
                :dbpath="'parser_data.PEParser.total_imports'"
              />
            </td>
            <td width="50%">
              <FilterDropDownMenu
                :field="'Export Count'"
                :value="item.total_exports"
                :displayFieldName="true"
                v-on="$listeners"
                :dbpath="'parser_data.PEParser.total_exports'"
              />
            </td>
          </tr>
        </tbody>
      </table>
      <br />
      <!-- #endregion General Information End -->

      <!-- #region Imports Sections start -->
      <div v-if="item.imports">
        <br />
        <b-card
          bg-variant="subparse-default"
          text-variant="white"
          header="Imports Sections"
          no-body
        >
            <div v-for="(imp, key) in getKeys(item.imports)" :key="key">
                <p class="card-header"> {{ imp }}</p>
                <FilterTable v-on="$listeners" :items="item.imports[imp]" :fields="getKeyFromList(item.imports[imp])" :leading="'parser_data.PEParser.imports.' + imp + '.'"/>
            </div>
        </b-card>
      </div>
      <br />
      <!-- #endregion Imports Sections end -->

      <!-- #region Code Sections start -->
      <div v-if="item.sections">
        <br />
        <b-card
          bg-variant="subparse-default"
          text-variant="white"
          header="Code Sections"
          no-body
        >
          <!-- note: filter table might need work on the dbpath, due to most of the data being in lists -->
          <FilterTable
            v-on="$listeners"
            :items="item.sections"
            :fields="field_data"
            leading="parser_data.PEParser.sections."
          />
        </b-card>
      </div>
      <br />
      <!-- #endregion Code Sections end -->
    </b-card>
  </div>
</template>


<script>
import FilterTable from "../utils/filterTable/FilterTable.vue";
import FilterDropDownMenu from "../utils/dropdown/FilterDropDownMenu.vue";
import * as Helpers from "../utils/helpers/Helpers";

export default {
  name: "peparser_view",
  data: function () {
    return {
      field_data: [
        "name",
        "virtual_address",
        "virtual_size",
        "section_raw_size",
        "read",
        "write",
        "execute",
        "contains_code",
        "contains_init",
        "entropy",
      ],
    };
  },
  components: {
    FilterTable,
    FilterDropDownMenu,
  },
  props: {
    /**
     * Elasticsearch PEParser item
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

<style scoped>
.pe-imports {
    background-color: teal;
}
</style>