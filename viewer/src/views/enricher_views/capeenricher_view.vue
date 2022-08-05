<template>
    <div>
        <b-card bg-variant="subparse-default" text-variant="white" header="CAPE Enricher" no-body>   
            <div v-if="item.status == 'reported'">
                <div v-if="item.report.info != {}">
                    <p class="card-header">General</p>
                    <table class="general">
                        <tr>
                            <td >
                                <FilterDropDownMenu
                                    :field="'Package'"
                                    :value="item.report.info.package"
                                    :displayFieldName="true"
                                    v-on="$listeners"
                                    :dbpath="'enricher_data.CAPEEnricher.report.info.package'"
                                />
                            </td>
                            <td >
                                <FilterDropDownMenu
                                    :field="'Version'"
                                    :value="item.report.info.version"
                                    :displayFieldName="true"
                                    v-on="$listeners"
                                    :dbpath="'enricher_data.CAPEEnricher.report.info.version'"
                                />
                            </td>
                            <td >
                                <FilterDropDownMenu
                                    :field="'Duration'"
                                    :value="item.report.info.duration"
                                    :displayFieldName="true"
                                    v-on="$listeners"
                                    :dbpath="'enricher_data.CAPEEnricher.report.info.duration'"
                                />
                            </td>
                        </tr>
                    </table>
                </div>

                <div v-if="item.report.target != {}">
                    <br/>
                    <table class="general">
                         <tr>
                            <td >
                                <FilterDropDownMenu
                                    :field="'Type'"
                                    :value="item.report.target.file.type"
                                    :displayFieldName="true"
                                    v-on="$listeners"
                                    :dbpath="'enricher_data.CAPEEnricher.report.target.file.type'"
                                />
                            </td>
                        </tr>
                        <tr>
                            <td >
                                <FilterDropDownMenu
                                    :field="'SHA-256'"
                                    :value="item.report.target.file.sha256"
                                    :displayFieldName="true"
                                    v-on="$listeners"
                                    :dbpath="'enricher_data.CAPEEnricher.report.target.file.sha256'"
                                />
                            </td>
                        </tr>
                        <tr>
                            <td >
                                <FilterDropDownMenu
                                    :field="'SHA-512'"
                                    :value="item.report.target.file.sha512"
                                    :displayFieldName="true"
                                    v-on="$listeners"
                                    :dbpath="'enricher_data.CAPEEnricher.report.target.file.sha512'"
                                />
                            </td>
                        </tr>
                    </table>
                </div>

                <!-- #region Office Meta Data : Start -->
                <div v-if="'office' in item.report.target.file">
                    <p class="card-header">Office Metadata</p>
                    <table class="general">
                        <tr>
                            <td >
                                <FilterDropDownMenu
                                    :field="'Created'"
                                    :value="item.report.target.file.office.Metadata.SummaryInformation.created"
                                    :displayFieldName="true"
                                    v-on="$listeners"
                                    :dbpath="'enricher_data.CAPEEnricher.report.target.file.office.Metadata.SummaryInformation.created'"
                                />
                            </td>
                            <td >
                                <FilterDropDownMenu
                                    :field="'Modified'"
                                    :value="item.report.target.file.office.Metadata.SummaryInformation.modified"
                                    :displayFieldName="true"
                                    v-on="$listeners"
                                    :dbpath="'enricher_data.CAPEEnricher.report.target.file.office.Metadata.SummaryInformation.modified'"
                                />
                            </td>
                        </tr>
                        <tr>
                            <td >
                                <FilterDropDownMenu
                                    :field="'App Version'"
                                    :value="item.report.target.file.office.Metadata.DocumentSummaryInformation.AppVersion"
                                    :displayFieldName="true"
                                    v-on="$listeners"
                                    :dbpath="'enricher_data.CAPEEnricher.report.target.file.office.Metadata.DocumentSummaryInformation.AppVersion'"
                                />
                            </td>
                            <td >
                                <FilterDropDownMenu
                                    :field="'Scale Crop'"
                                    :value="item.report.target.file.office.Metadata.DocumentSummaryInformation.ScaleCrop"
                                    :displayFieldName="true"
                                    v-on="$listeners"
                                    :dbpath="'enricher_data.CAPEEnricher.report.target.file.office.Metadata.DocumentSummaryInformation.ScaleCrop'"
                                />
                            </td>
                            <td >
                                <FilterDropDownMenu
                                    :field="'Doc Security'"
                                    :value="item.report.target.file.office.Metadata.DocumentSummaryInformation.DocSecurity"
                                    :displayFieldName="true"
                                    v-on="$listeners"
                                    :dbpath="'enricher_data.CAPEEnricher.report.target.file.office.Metadata.DocumentSummaryInformation.DocSecurity'"
                                />
                            </td>
                            <td >
                                <FilterDropDownMenu
                                    :field="'Links Up To Date'"
                                    :value="item.report.target.file.office.Metadata.DocumentSummaryInformation.LinksUpToDate"
                                    :displayFieldName="true"
                                    v-on="$listeners"
                                    :dbpath="'enricher_data.CAPEEnricher.report.target.file.office.Metadata.DocumentSummaryInformation.LinksUpToDate'"
                                />
                            </td>
                        </tr>
                        <tr>
                            <td >
                                <FilterDropDownMenu
                                    :field="'Hyperlinks Changed'"
                                    :value="item.report.target.file.office.Metadata.DocumentSummaryInformation.HyperlinksChanged"
                                    :displayFieldName="true"
                                    v-on="$listeners"
                                    :dbpath="'enricher_data.CAPEEnricher.report.target.file.office.Metadata.DocumentSummaryInformation.HyperlinksChanged'"
                                />
                            </td>
                            <td >
                                <FilterDropDownMenu
                                    :field="'Application'"
                                    :value="item.report.target.file.office.Metadata.DocumentSummaryInformation.Application"
                                    :displayFieldName="true"
                                    v-on="$listeners"
                                    :dbpath="'enricher_data.CAPEEnricher.report.target.file.office.Metadata.DocumentSummaryInformation.Application'"
                                />
                            </td>
                            <td >
                                <FilterDropDownMenu
                                    :field="'Shared Doc'"
                                    :value="item.report.target.file.office.Metadata.DocumentSummaryInformation.SharedDoc"
                                    :displayFieldName="true"
                                    v-on="$listeners"
                                    :dbpath="'enricher_data.CAPEEnricher.report.target.file.office.Metadata.DocumentSummaryInformation.SharedDoc'"
                                />
                            </td>
                            <td >
                                <FilterDropDownMenu
                                    :field="'Has Macros'"
                                    :value="item.report.target.file.office.Metadata.HasMacros"
                                    :displayFieldName="true"
                                    v-on="$listeners"
                                    :dbpath="'enricher_data.CAPEEnricher.report.target.file.office.Metadata.HasMacros'"
                                />
                            </td>
                        </tr>
                    </table>
                </div>
                <!-- #endregion Office Meta Data : End -->

                <!-- #region PE Data : Start -->
                <div v-if="'pe' in item.report.target.file">
                    <p class="card-header">PE Data</p>
                    <table class="general">
                        <tr>
                            <td >
                                <FilterDropDownMenu
                                    :field="'Image Base'"
                                    :value="item.report.target.file.pe.imagebase"
                                    :displayFieldName="true"
                                    v-on="$listeners"
                                    :dbpath="'enricher_data.CAPEEnricher.report.target.file.pe.imagebase'"
                                />
                            </td>
                            <td >
                                <FilterDropDownMenu
                                    :field="'Entry Point'"
                                    :value="item.report.target.file.pe.entrypoint"
                                    :displayFieldName="true"
                                    v-on="$listeners"
                                    :dbpath="'enricher_data.CAPEEnricher.report.target.file.pe.entrypoint'"
                                />
                            </td>
                            <td >
                                <FilterDropDownMenu
                                    :field="'Actual Checksum'"
                                    :value="item.report.target.file.pe.actual_checksum"
                                    :displayFieldName="true"
                                    v-on="$listeners"
                                    :dbpath="'enricher_data.CAPEEnricher.report.target.file.pe.actual_checksum'"
                                />
                            </td>
                        </tr>
                    </table>

                    <br/>
                    <p class="card-header">PE Imports</p>
                    <div v-for="(imp, key) in getKeys(item.report.target.file.pe.imports)" :key="key">
                        <p class="card-header">PE Import - {{ imp }}</p>
                        <FilterTable v-on="$listeners" :items="item.report.target.file.pe.imports[imp].imports" :fields="getKeyFromList(item.report.target.file.pe.imports[imp].imports)" :leading="'enricher_data.CAPEEnricher.report.target.file.pe.imports.' + imp + '.'"/>
                    </div>

                    <br/>
                    <p class="card-header">PE Dirents</p>
                    <FilterTable
                        v-on="$listeners"
                        :items="item.report.target.file.pe.dirents"
                        :fields="getKeyFromList(item.report.target.file.pe.dirents)"
                        leading="enricher_data.CAPEEnricher.report.target.file.pe.dirents."
                    />

                    <br/>
                    <p class="card-header">PE Sections</p>
                    <FilterTable
                        v-on="$listeners"
                        :items="item.report.target.file.pe.sections"
                        :fields="getKeyFromList(item.report.target.file.pe.sections)"
                        leading="enricher_data.CAPEEnricher.report.target.file.pe.sections."
                    />


                    <br/>
                    <p class="card-header">PE Resources</p>
                    <FilterTable
                        v-on="$listeners"
                        :items="item.report.target.file.pe.resources"
                        :fields="getKeyFromList(item.report.target.file.pe.resources)"
                        leading="enricher_data.CAPEEnricher.report.target.file.pe.resources."
                    />

                    <div v-if="item.report.payloads.length != 0">
                        <br/>
                        <p class="card-header">PE Payloads</p>
                        <div v-for="(payload, key) in item.report.payloads" :key="key">
                            <p class="card-header">Payload :: {{payload.name}}</p>
                            <table class="general">
                                <tr>
                                    <td >
                                        <FilterDropDownMenu
                                            :field="'Name'"
                                            :value="payload.name"
                                            :displayFieldName="true"
                                            v-on="$listeners"
                                            :dbpath="'enricher_data.CAPEEnricher.report.payloads.name'"
                                        />
                                    </td>
                                </tr>

                                <tr>
                                    <FilterDropDownMenu
                                        :field="'Cape Type'"
                                        :value="payload.cape_type"
                                        :displayFieldName="true"
                                        v-on="$listeners"
                                        :dbpath="'enricher_data.CAPEEnricher.report.payloads.cape_type'"
                                    />
                                    <FilterDropDownMenu
                                        :field="'Type'"
                                        :value="payload.type"
                                        :displayFieldName="true"
                                        v-on="$listeners"
                                        :dbpath="'enricher_data.CAPEEnricher.report.payloads.type'"
                                    />
                                    <FilterDropDownMenu
                                        :field="'Process Name'"
                                        :value="payload.process_name"
                                        :displayFieldName="true"
                                        v-on="$listeners"
                                        :dbpath="'enricher_data.CAPEEnricher.report.payloads.process_name'"
                                    />
                                </tr>
                                <tr>
                                    <td>
                                        <FilterDropDownMenu
                                            :field="'Host Path'"
                                            :value="payload.path"
                                            :displayFieldName="true"
                                            v-on="$listeners"
                                            :dbpath="'enricher_data.CAPEEnricher.report.payloads.path'"
                                        />
                                    </td>
                                </tr>

                                <tr>
                                    <td>
                                        <FilterDropDownMenu
                                            :field="'SHA1'"
                                            :value="payload.sha1"
                                            :displayFieldName="true"
                                            v-on="$listeners"
                                            :dbpath="'enricher_data.CAPEEnricher.report.payloads.sha1'"
                                        />
                                    </td>
                                </tr>
                                <tr>
                                    <td>
                                        <FilterDropDownMenu
                                            :field="'SHA512'"
                                            :value="payload.sha512"
                                            :displayFieldName="true"
                                            v-on="$listeners"
                                            :dbpath="'enricher_data.CAPEEnricher.report.payloads.sha512'"
                                        />
                                    </td>
                                </tr>
                                <tr>
                                    <td>
                                        <FilterDropDownMenu
                                            :field="'SSDeep'"
                                            :value="payload.ssdeep"
                                            :displayFieldName="true"
                                            v-on="$listeners"
                                            :dbpath="'enricher_data.CAPEEnricher.report.payloads.ssdeep'"
                                        />
                                    </td>
                                </tr>
                            </table>
                            <br/>
                        </div>
                    </div>
                    
                </div>
                <!-- #endregion PE Data : End -->

                
            </div>
            <div v-if="item.status != 'reported'">
                 <tbody>
                        <tr>
                            <td width="50%"><strong>Status: </strong>{{ item.status }}</td>
                        </tr>
                </tbody>
            </div>
        </b-card>
    </div>
</template>

<script>
    import FilterTable from "../utils/filterTable/FilterTable.vue";
    import FilterDropDownMenu from "../utils/dropdown/FilterDropDownMenu.vue";
    import * as Helpers from "../utils/helpers/Helpers";

    export default {
        name: "capeenricher_view",
        data: function() {
            /**
             * View default values for tables
             */
            return {
                section_data: [
                    "name",
                    "size_of_data",
                    "virtual_address",
                    "characteristics",
                    "characteristics_raw",
                    "entropy",
                    "virtual_size",
                    "raw_address",
                ],
                export_data: [
                    "name",
                    "address",
                    "ordinal",
                ],
                import_data: [
                    "name",
                    "address",
                ],
                version_data: [
                    "name",
                    "value",
                ],
            }
        },
        components: {
            FilterTable,
            FilterDropDownMenu
        },
        props: {
            /**
             * CAPE V2 Enricher item data
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
