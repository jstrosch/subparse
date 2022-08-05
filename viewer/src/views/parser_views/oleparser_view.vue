<template>
  <div v-if="
        item.rtf.length != 0 
      || Object.keys(item.meta_data).length != 0 
      || item.times.length != 0 
      || item.indicators.length != 0 
      || Object.keys(item.vba).length != 0 
      || Object.keys(item.mraptor).length != 0 
      || Object.keys(item.ole_obj).length != 0 ">
    <b-card
      bg-variant="subparse-default"
      text-variant="white"
      header="OLE Parser"
      no-body
    >
        <!-- #region RTF Data Start -->  
        <div v-if="item.rtf.length != 0">
          <br />
          <p class="card-header">RTF</p>
          <FilterTable v-on="$listeners" :items="item.rtf" :fields="rtf_fields" :leading="'parser_data.OLEParser.rtf.'"/>
        </div>
        <!-- #endregion RTF Data Start -->  

        <!-- #region (OLEMETA) Meta data Start -->
        <div v-if="Object.keys(item.meta_data).length != 0"> 
          <div v-if="getKeysNoneNull(item.meta_data.doc_summary).length != 0"> 
            <br />
            <p class="card-header">OLEMETA Doc Summary</p>
            <FilterTable v-on="$listeners" :items="[item.meta_data.doc_summary]" :fields="getKeysNoneNull(item.meta_data.doc_summary)" :leading="'parser_data.OLEParser.meta_data.doc_summary.'"/>
          </div>
          <div v-if="getKeysNoneNull(item.meta_data.summary_attribs).length != 0">
            <br />
            <p class="card-header">OLEMETA Summary</p>
            <FilterTable v-on="$listeners" :items="[item.meta_data.summary_attribs]" :fields="getKeysNoneNull(item.meta_data.summary_attribs)" :leading="'parser_data.OLEParser.meta_data.summary_attribs.'"/>        
          </div>
        </div>
        <!-- #endregion (OLEMETA) Meta data End -->

        <!-- #region (OLETIMES) Time Start -->
        <div v-if="item.times.length != 0">
          <br />
          <p class="card-header">OLETIMES</p>
          <FilterTable v-on="$listeners" :items="item.times" :fields="getKeyFromList(item.times)" :leading="'parser_data.OLEParser.times.'"/>
        </div>
        <!-- #endregion (OLETIMES) Time End -->

        <!-- #region (OLEID) Indicators Start -->
        <div v-if="item.indicators.length != 0">
          <br />
          <p class="card-header">OLEID</p>
          <FilterTable v-on="$listeners" :items="item.indicators" :fields="getKeyFromList(item.indicators)" :leading="'parser_data.OLEParser.indicators.'"/>
        </div>
        <!-- #endregion (OLEID) Indicators Start -->

        <!-- #region (OLEVBA) Start -->
        <div v-if="Object.keys(item.vba).length != 0"> 
          <br />
          <p class="card-header">OLEVBA</p>
          <table class="general">
            <tbody>
              <tr>
                <td width="50%">
                  <FilterDropDownMenu
                    :field="'Auto Exec'"
                    :value="item.vba.macros.general.auto_exec"
                    :displayFieldName="true"
                    v-on="$listeners"
                    :dbpath="'parser_data.OLEParser.vba.macros.general.auto_exec'"
                  />
                </td>
                <td width="50%">
                  <FilterDropDownMenu
                    :field="'Suspicious'"
                    :value="item.vba.macros.general.suspicious"
                    :displayFieldName="true"
                    v-on="$listeners"
                    :dbpath="'parser_data.OLEParser.vba.macros.general.suspicious'"
                  />
                </td>
              </tr>
              
              <tr>
                <td width="50%">
                  <FilterDropDownMenu
                    :field="'IOC'"
                    :value="item.vba.macros.general.ioc"
                    :displayFieldName="true"
                    v-on="$listeners"
                    :dbpath="'parser_data.OLEParser.vba.macros.general.ioc'"
                  />
                </td>
                <td width="50%">
                  <FilterDropDownMenu
                    :field="'Hex Obfuscated'"
                    :value="item.vba.macros.general.hex_obfuscated"
                    :displayFieldName="true"
                    v-on="$listeners"
                    :dbpath="'parser_data.OLEParser.vba.macros.general.hex_obfuscated'"
                  />
                </td>
              </tr>

              <tr>
                <td width="50%">
                  <FilterDropDownMenu
                    :field="'Base Obfuscated'"
                    :value="item.vba.macros.general.base_obfuscated"
                    :displayFieldName="true"
                    v-on="$listeners"
                    :dbpath="'parser_data.OLEParser.vba.macros.general.base_obfuscated'"
                  />
                </td>
                <td width="50%">
                  <FilterDropDownMenu
                    :field="'Dridex Obfuscated'"
                    :value="item.vba.macros.general.dridex_obfuscated"
                    :displayFieldName="true"
                    v-on="$listeners"
                    :dbpath="'parser_data.OLEParser.vba.macros.general.dridex_obfuscated'"
                  />
                </td>
              </tr>

              <tr>
                <td width="50%">
                  <FilterDropDownMenu
                    :field="'VBA Obfuscated'"
                    :value="item.vba.macros.general.vba_obfuscated"
                    :displayFieldName="true"
                    v-on="$listeners"
                    :dbpath="'parser_data.OLEParser.vba.macros.general.vba_obfuscated'"
                  />
                </td>
              </tr>

            </tbody>
          </table>

          <p class="card-header">Macro Abilities</p>
          <FilterTable v-on="$listeners" :items="item.vba.macros.macro_abilities" :fields="getKeyFromList(item.vba.macros.macro_abilities)" :leading="'parser_data.OLEParser.vba.macros.macro_abilities.'"/>

          <p class="card-header">Macros</p>
          <div v-for="(macro, key) in getKeys(item.vba.macros.macros)" :key="key">
            <p class="card-header">Macros :: {{ item.vba.macros.macros[macro].filename }}</p>
            <table class="general">
              <tbody>
                <tr>
                  <td width="50%">
                    <FilterDropDownMenu
                      :field="'OLE Stream'"
                      :value="item.vba.macros.macros[macro].ole_stream"
                      :displayFieldName="true"
                      v-on="$listeners"
                      :dbpath="'parser_data.PEParser.pe_signature'"
                    />
                  </td>
                </tr>
              </tbody>
            </table>
            <FilterTable v-on="$listeners" :items="[item.vba.macros.macros[macro].code]" :fields="getKeys(item.vba.macros.macros[macro].code)" :leading="'parser_data.OLEParser.vba.macros.code.code.'"/>
            <br/>
          </div>
        </div>

        <!-- #endregion (OLEVBA) End -->

        <!-- #region (MRAPTOR) Macro Atrs. Start -->
        <div v-if="Object.keys(item.mraptor).length != 0">
          <br />
          <p class="card-header">MRAPTOR</p>
          <table class="general">
            <tbody>
              <tr>
                <td width="50%">
                  <FilterDropDownMenu
                    :field="'Macro Type'"
                    :value="item.mraptor.macro_type"
                    :displayFieldName="true"
                    v-on="$listeners"
                    :dbpath="'parser_data.OLEParser.mraptor.macro_type'"
                  />
                </td>
                <td width="50%">
                  <FilterDropDownMenu
                    :field="'File Type'"
                    :value="item.mraptor.file_type"
                    :displayFieldName="true"
                    v-on="$listeners"
                    :dbpath="'parser_data.OLEParser.mraptor.file_type'"
                  />
                </td>
              </tr>
            </tbody>
          </table>
          <p class="card-header">MRAPTOR :: Flags</p>
          <FilterTable v-on="$listeners" :items="item.mraptor.macro_flags" :fields="getKeyFromList(item.mraptor.macro_flags)" :leading="'parser_data.OLEParser.mraptor.macro_flags.'"/>
        </div>
        <!-- #endregion (MRAPTOR) Macro Atrs. End -->

        <div v-if="Object.keys(item.ole_obj).length != 0">
          <!-- #region (OLEOBJ) Links Start -->
            <div v-if="Object.keys(item.ole_obj.links).length != 0">
              <br />
              <p class="card-header">Links Found</p>
              <!-- <p> {{ Object.keys(item.ole_obj.links) }}</p> -->
              <div v-for="(link, key) in Object.keys(item.ole_obj.links)" :key="key">
                <div v-if="item.ole_obj.links[link] != 0">
                  <FilterTable v-on="$listeners" :items="item.ole_obj.links[link]" :fields="[link]" :leading="'parser_data.OLEParser.ole_obj.links.'"/>
                </div>
              </div>
            </div>
          <!-- #endregion (OLEOBJ) Links End -->

          <!-- #region (OLEOBJ) Files Found Start -->
          <div v-if="item.ole_obj.embedded.length != 0">
            <br />
            <p class="card-header">Embedded Files</p>
            <FilterTable v-on="$listeners" :items="item.ole_obj.embedded" :fields="getKeyFromList(item.ole_obj.embedded)" :leading="'parser_data.OLEParser.ole_obj.embedded.'"/>
          </div>
          <!-- #endregion (OLEOBJ) Files Found End -->
        </div>
    </b-card>
  </div>
</template>


<script>
import FilterTable from "../utils/filterTable/FilterTable.vue";
import FilterDropDownMenu from "../utils/dropdown/FilterDropDownMenu.vue";
import * as Helpers from "../utils/helpers/Helpers";

export default {
  name: "oleparser_view",
  data: function () {
    return {
      rtf_fields: [
        "start",
        "end",
        "format_type",
        "oledata_size",
        "class_name",
        "is_package",
        "cve",
        "clsid"
      ],
    };
  },
  components: {
    FilterTable,
    FilterDropDownMenu,
  },
  props: {
    /**
     * Elasticsearch OLEParser item
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