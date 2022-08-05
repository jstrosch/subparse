<template>
    <div> 
        <b-card bg-variant="subparse-default" text-variant="white" header="Abuse Enricher" no-body>    
            <!-- #region General Information start -->
            <br />    
            <table class="general">
                <tbody>
                    <tr>
                        <td width="50%"><FilterDropDownMenu :field="'Abuse Signature'" :value="item.AbuseCHSignature" :displayFieldName="true" v-on="$listeners" :dbpath="'enricher_data.ABUSEEnricher.AbuseCHSignature'"/></td>
                        <td width="50%"><FilterDropDownMenu :field="'Origin Country'" :value="item.AbuseCHData.origin_country" :displayFieldName="true" v-on="$listeners" :dbpath="'enricher_data.ABUSEEnricher.AbuseCHData.origin_country'"/></td>
                    </tr>

                    <tr>
                        <td width="50%"><FilterDropDownMenu :field="'First Seen'" :value="item.AbuseCHData.first_seen !== null ? item.AbuseCHData.first_seen : 'N/A'" :displayFieldName="true" v-on="$listeners" :dbpath="'enricher_data.ABUSEEnricher.AbuseCHData.first_seen'"/></td>
                        <td width="50%"><FilterDropDownMenu :field="'Last Seen'" :value="item.AbuseCHData.last_seen !== null ? item.AbuseCHData.last_seen : 'N/A'" :displayFieldName="true" v-on="$listeners" :dbpath="'enricher_data.ABUSEEnricher.AbuseCHData.last_seen'"/></td>
                    </tr>

                    <tr>
                        <td width="50%"><FilterDropDownMenu :field="'Delivery Method'" :value="item.AbuseCHData.delivery_method !== null ? item.AbuseCHData.delivery_method : 'N/A'" :displayFieldName="true" v-on="$listeners" :dbpath="'enricher_data.ABUSEEnricher.AbuseCHData.delivery_method'"/></td>
                        <td width="50%"><FilterDropDownMenu :field="'File Type'" :value="item.AbuseCHData.file_type" :displayFieldName="true" v-on="$listeners" :dbpath="'enricher_data.ABUSEEnricher.AbuseCHData.file_type'"/></td>
                    </tr>

                </tbody>
            </table>
            <!-- #endregion General Information end -->

            <!-- #region vxCube start -->
            <div v-if="item.AbuseCHData.vendor_intel.vxCube">
                <br/>
                <b-card bg-variant="subparse-default" text-variant="white" header="vxCube" no-body>  
                    <br />
                    <table class="general">
                        <tbody>
                            <td width="50%"><FilterDropDownMenu :field="'Verdict'" :value="item.AbuseCHData.vendor_intel.vxCube.verdict !== null ? item.AbuseCHData.vendor_intel.vxCube.verdict : 'N/A'" :displayFieldName="true" v-on="$listeners" :dbpath="'enricher_data.ABUSEEnricher.AbuseCHData.vendor_intel.vxCube.verdict'"/></td>
                            <td width="50%"><FilterDropDownMenu :field="'Maliciousness'" :value="item.AbuseCHData.vendor_intel.vxCube.maliciousness !== null ? item.AbuseCHData.vendor_intel.vxCube.maliciousness : 'N/A'" :displayFieldName="true" v-on="$listeners" :dbpath="'enricher_data.ABUSEEnricher.AbuseCHData.vendor_intel.vxCube.maliciousness'"/></td>
                        </tbody>
                    </table>
                    <FilterTable v-if="item.AbuseCHData.vendor_intel.vxCube.behaviour" v-on="$listeners" :items="item.AbuseCHData.vendor_intel.vxCube.behaviour" :fields="behavior_fields" leading="enricher_data.ABUSEEnricher.AbuseCHData.vendor_intel.vxCube.behaviour" :searchInList="true"/>
                </b-card>
            </div>
            <!-- #endregion vxCube end -->

            <!-- Triage start -->
            <div v-if="item.AbuseCHData.vendor_intel.Triage">
                <br />
                <b-card bg-variant="subparse-default" text-variant="white" header="Triage" no-body>  
                    <br />
                    <table class="general">
                        <tbody>
                            <td width="50%"><FilterDropDownMenu :field="'Score'" :value="item.AbuseCHData.vendor_intel.Triage.score !== null ? item.AbuseCHData.vendor_intel.Triage.score : 'N/A'" :displayFieldName="true" v-on="$listeners" :dbpath="'enricher_data.ABUSEEnricher.AbuseCHData.vendor_intel.Triage.score'"/></td>
                            <td width="50%"><strong>Triage Link: </strong><a :href="`${item.AbuseCHData.vendor_intel.Triage.link}`" target="_blank" >{{ item.AbuseCHData.vendor_intel.Triage.link }}</a></td>
                        </tbody>
                    </table>
                    <FilterTable v-if="item.AbuseCHData.vendor_intel.Triage.signatures" v-on="$listeners" :items="item.AbuseCHData.vendor_intel.Triage.signatures" :fields="signature_fields" leading="enricher_data.ABUSEEnricher.AbuseCHData.vendor_intel.Triage.signatures" :searchInList="true"/>
                </b-card>
            </div>
            <!-- Triage end -->

            <!-- Yara Rules start -->
            <div v-if="item.AbuseCHData.yara_rules">
                <br />
                <b-card bg-variant="subparse-default" text-variant="white" header="Yara Rules" no-body>  
                    <br />
                    <FilterTable v-if="item.AbuseCHData.yara_rules" v-on="$listeners" :items="item.AbuseCHData.yara_rules" :fields="yara_fields" leading="enricher_data.ABUSEEnricher.AbuseCHData.yara_rules" :searchInList="true"/>
                </b-card>
            </div>
            <!-- Triage end -->

        </b-card>
    </div>
</template>


<script>
    import FilterTable from "../utils/filterTable/FilterTable.vue";
    import FilterDropDownMenu from "../utils/dropdown/FilterDropDownMenu.vue";

    export default {
        name: "abuseenricher_view",
        data: function() {
            /**
             * View default values for tables
             */
            return {
                behavior_fields: ["threat_level", "rule"],
                yara_fields: ["rule_name", "author", "description", "reference"],
                signature_fields: ["signature", "score"],
            }
        },
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
    };
</script>