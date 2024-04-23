<template>
    <div> 
        <b-card text-variant="white" header="Yara Enricher" no-body>    
            <table class="general">
                <tbody>
                    <!-- General Information --> 
                    <tr>
                        <td >
                            <FilterDropDownMenu
                                :field="'Rules File'"
                                :value="item.yara_file"
                                :displayFieldName="true"
                                v-on="$listeners"
                                :dbpath="'enricher_data.YARAEnricher.yara_file'"
                            />
                        </td>
                    </tr>
                </tbody>
            </table>

            <div v-if="item.matched.length != 0">
                <p class="card-header">Matched Rules</p>
                <div v-for="(match, key) in item.matched" :key="key">
                    <p class="card-header">Rule :: {{ match.rule }}</p>
                    <FilterTable v-on="$listeners" :items="[match.meta_data]" :fields="getKeys(match.meta_data)" :leading="'SUBFILTER.enricher_data.YARAEnricher.matched.meta_data.'"/>
                    <div v-if="match.tags.length != 0">
                        <div v-for="(tag, key1) in match.tags" :key="key1">
                            <FilterDropDownMenu
                                    :field="'Tag'"
                                    :value="tag"
                                    :displayFieldName="true"
                                    v-on="$listeners"
                                    :dbpath="'SUBFILTER.enricher_data.YARAEnricher.matched.tags'"
                                />
                        </div>
                    </div>
                    <br/>
                    <br/>
                </div>
            </div>
            
            
        </b-card>
    </div>
</template>


<script>
    import FilterTable from "../utils/filterTable/FilterTable.vue";
    import FilterDropDownMenu from "../utils/dropdown/FilterDropDownMenu.vue";
    import * as Helpers from "../utils/helpers/Helpers";

    export default {
        name: "yaraenricher_view",
        components: {
            FilterTable,
            FilterDropDownMenu
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