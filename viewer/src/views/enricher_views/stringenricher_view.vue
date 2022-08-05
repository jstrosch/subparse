<template>
    <div> 
        <b-card bg-variant="subparse-default" text-variant="white" header="String Enricher" no-body>    
            <!-- #region String Output start -->
            <br/>    
            <div v-for="(type, key) in item" :key="key">
                <div v-if="type.length != 0">
                    <p class="card-header">{{strings_dir_match[key]}}</p>
                    <FilterTable v-if="type.length != 0" v-on="$listeners" :items="cleanList(type, key)" :fields="[key]" leading="SUBFILTER.enricher_data.STRINGEnricher."/>
                    <br/>
                </div>
            </div>
            <!-- #endregion String Output end -->
        </b-card>
    </div>
</template>


<script>
    import FilterTable from "../utils/filterTable/FilterTable.vue";
    import * as Helpers from "../utils/helpers/Helpers";

    export default {
        name: "stringenricher_view",
        data: function() {
            /**
             * View default values for tables
             */
            return {
                string_fields: ["Strings"],
                strings_dir_match: {
                    'audio': 'Audio',
                    'code': 'Code',
                    'command_line_arguments': 'Command Line Arguments',
                    'compressed': 'Compressed',
                    'exec_files': 'Exec Files',
                    'misc_files': 'Misc. Files',
                    'images': 'Images',
                    'ip': 'IP',
                    'ip_port': 'IP : Port',
                    'web': 'Web',
                    'work': 'Work'
                }
            }
        },
        components: {
            FilterTable,
            // FilterDropDownMenu
        },
        props: {
            /**
             * Abuse Enricher item data
             */
            item: {
                type: Object,
                required: true,
            }
        },
        methods: {
           ...Helpers
        }
    };
</script>