<template>
    <!-- #region Error -->
    <div v-if="hasError">
        <h1>ERROR</h1>
    </div>
    <!-- #endregion Error End-->
    <div v-else>
        <b-card
            bg-variant="dark"
            text-variant="white"
            header="ELF Parser"
            no-body
            >
            <!-- #region General ELF Information --> 
            <b-card
                bg-variant="success"
                text-variant="white"
                header="General ELF Information"
                no-body
            >   
                <table class="general">
                    <tr>
                        <td width="33%">
                            <FilterDropDownMenu
                                :field="'EI Data'"
                                :value="item.general_info.ei_data"
                                :displayFieldName="true"
                                v-on="$listeners"
                                :dbpath="'parser_data.ELFParser.general_info.ei_data'"
                            />
                        </td>
                        <td width="33%">
                            <FilterDropDownMenu
                                :field="'EI Version'"
                                :value="item.general_info.ei_version"
                                :displayFieldName="true"
                                v-on="$listeners"
                                :dbpath="'parser_data.ELFParser.general_info.ei_version'"
                            />
                        </td>
                        <td width="33%">
                            <FilterDropDownMenu
                                :field="'EI OSABI'"
                                :value="item.general_info.ei_osabi"
                                :displayFieldName="true"
                                v-on="$listeners"
                                :dbpath="'parser_data.ELFParser.general_info.ei_osabi'"
                            />
                        </td>
                    </tr>


                    <tr>
                        <td width="33%">
                            <FilterDropDownMenu
                                :field="'EI Abiversion'"
                                :value="item.general_info.ei_abiversion"
                                :displayFieldName="true"
                                v-on="$listeners"
                                :dbpath="'parser_data.ELFParser.general_info.ei_abiversion'"
                            />
                        </td>
                        <td width="33%">
                            <FilterDropDownMenu
                                :field="'EI Type'"
                                :value="item.general_info.e_type"
                                :displayFieldName="true"
                                v-on="$listeners"
                                :dbpath="'parser_data.ELFParser.general_info.e_type'"
                            />
                        </td>
                        <td width="33%">
                            <FilterDropDownMenu
                                :field="'EI Machine'"
                                :value="item.general_info.e_machine"
                                :displayFieldName="true"
                                v-on="$listeners"
                                :dbpath="'parser_data.ELFParser.general_info.e_machine'"
                            />
                        </td>
                    </tr>

                    <tr>
                        <td width="33%">
                            <FilterDropDownMenu
                                :field="'EI Version #'"
                                :value="item.general_info.e_version_numeric"
                                :displayFieldName="true"
                                v-on="$listeners"
                                :dbpath="'parser_data.ELFParser.general_info.e_version_numeric'"
                            />
                        </td>
                        <td width="33%">
                            <FilterDropDownMenu
                                :field="'Entry Point'"
                                :value="item.general_info.entry_point"
                                :displayFieldName="true"
                                v-on="$listeners"
                                :dbpath="'parser_data.ELFParser.general_info.entry_point'"
                            />
                        </td>
                        <td width="33%">
                            <FilterDropDownMenu
                                :field="'Headers Start'"
                                :value="item.general_info.program_headers_start"
                                :displayFieldName="true"
                                v-on="$listeners"
                                :dbpath="'parser_data.ELFParser.general_info.program_headers_start'"
                            />
                        </td>
                    </tr>

                    <tr>
                        <td width="33%">
                            <FilterDropDownMenu
                                :field="'Sections Start'"
                                :value="item.general_info.program_sections_start"
                                :displayFieldName="true"
                                v-on="$listeners"
                                :dbpath="'parser_data.ELFParser.general_info.program_sections_start'"
                            />
                        </td>
                        <td width="33%">
                            <FilterDropDownMenu
                                :field="'Flags Hex'"
                                :value="item.general_info.flags_hex"
                                :displayFieldName="true"
                                v-on="$listeners"
                                :dbpath="'parser_data.ELFParser.general_info.flags_hex'"
                            />
                        </td>
                        <td width="33%">
                            <FilterDropDownMenu
                                :field="'Flags Decoded'"
                                :value="item.general_info.flags_decoded"
                                :displayFieldName="true"
                                v-on="$listeners"
                                :dbpath="'parser_data.ELFParser.general_info.flags_decoded'"
                            />
                        </td>
                    </tr>

                    <tr>
                        <td width="33%">
                            <FilterDropDownMenu
                                :field="'EH Size'"
                                :value="item.general_info.e_ehsize"
                                :displayFieldName="true"
                                v-on="$listeners"
                                :dbpath="'parser_data.ELFParser.general_info.e_ehsize'"
                            />
                        </td>
                        <td width="33%">
                            <FilterDropDownMenu
                                :field="'PHeader Size'"
                                :value="item.general_info.e_pheadersize"
                                :displayFieldName="true"
                                v-on="$listeners"
                                :dbpath="'parser_data.ELFParser.general_info.e_pheadersize'"
                            />
                        </td>
                        <td width="33%">
                            <FilterDropDownMenu
                                :field="'PHeader Number'"
                                :value="item.general_info.e_phnum"
                                :displayFieldName="true"
                                v-on="$listeners"
                                :dbpath="'parser_data.ELFParser.general_info.e_phnum'"
                            />
                        </td>
                    </tr>

                    <tr>
                        <td width="33%">
                            <FilterDropDownMenu
                                :field="'SHeader Size'"
                                :value="item.general_info.e_sheadersize"
                                :displayFieldName="true"
                                v-on="$listeners"
                                :dbpath="'parser_data.ELFParser.general_info.e_sheadersize'"
                            />
                        </td>
                        <td width="33%">
                            <FilterDropDownMenu
                                :field="'SHeader Size'"
                                :value="item.general_info.e_shnum"
                                :displayFieldName="true"
                                v-on="$listeners"
                                :dbpath="'parser_data.ELFParser.general_info.e_shnum'"
                            />
                        </td>
                        <td width="33%">
                            <FilterDropDownMenu
                                :field="'Number Of Sections'"
                                :value="item.general_info.e_numsections"
                                :displayFieldName="true"
                                v-on="$listeners"
                                :dbpath="'parser_data.ELFParser.general_info.e_numsections'"
                            />
                        </td>
                    </tr>

                    <tr>
                        <td width="33%">
                            <FilterDropDownMenu
                                :field="'E_SHSTRNDX'"
                                :value="item.general_info.e_shstrndx"
                                :displayFieldName="true"
                                v-on="$listeners"
                                :dbpath="'parser_data.ELFParser.general_info.e_shstrndx'"
                            />
                        </td>
                        <td width="33%">
                            <FilterDropDownMenu
                                :field="'SHSTRNDX'"
                                :value="item.general_info.shstrndx"
                                :displayFieldName="true"
                                v-on="$listeners"
                                :dbpath="'parser_data.ELFParser.general_info.shstrndx'"
                            />
                        </td>
                        <td width="33%">
                            <FilterDropDownMenu
                                :field="'Magic Bytes'"
                                :value="item.general_info.magic_bytes"
                                :displayFieldName="true"
                                v-on="$listeners"
                                :dbpath="'parser_data.ELFParser.general_info.magic_bytes'"
                            />
                        </td>
                    </tr>
                </table>
            </b-card>
            <!-- #endregion General ELF Information End --> 

            <!-- #region Version Info -->
            <div v-if="item.version_info != null">
                <br/>
                <b-card
                    bg-variant="secondary"
                    text-variant="white"
                    no-body 
                    header="Version Information" >
                
                    <div v-for="(verinfo, key) in this.getKeys(item.version_info)" :key="key">
                        <br/>
                        <table class="general">
                            <tr>
                                <td width="33%">
                                    <FilterDropDownMenu
                                        :field="'Type'"
                                        :value="item.version_info[verinfo].type != null ? item.version_info[verinfo].type : 'None'"
                                        :displayFieldName="true"
                                        v-on="$listeners"
                                        :dbpath="'parser_data.ELFParser.version_info.' + verinfo + '.type'"
                                    />
                                </td>
                                <td width="33%">
                                    <FilterDropDownMenu
                                        :field="'Entry Count'"
                                        :value="item.version_info[verinfo].entry_count != null ? item.version_info[verinfo].entry_count : 'None'"
                                        :displayFieldName="true"
                                        v-on="$listeners"
                                        :dbpath="'parser_data.ELFParser.version_info.' + verinfo + '.entry_count'"
                                    />
                                </td>
                                <td width="33%">
                                    <FilterDropDownMenu
                                        :field="'Link'"
                                        :value="item.version_info[verinfo].link != null ? item.version_info[verinfo].link : 'None'"
                                        :displayFieldName="true"
                                        v-on="$listeners"
                                        :dbpath="'parser_data.ELFParser.version_info.' + verinfo + '.link'"
                                    />
                                </td>
                            </tr>
                            <tr>
                                <td width="33%">
                                    <FilterDropDownMenu
                                        :field="'Link Name'"
                                        :value="item.version_info[verinfo].link_name != null ? item.version_info[verinfo].link_name : 'None'"
                                        :displayFieldName="true"
                                        v-on="$listeners"
                                        :dbpath="'parser_data.ELFParser.version_info.' + verinfo + '.link_name'"
                                    />
                                </td>
                                <td width="33%">
                                    <FilterDropDownMenu
                                        :field="'Off Set'"
                                        :value="item.version_info[verinfo].offset != null ? item.version_info[verinfo].offset : 'None'"
                                        :displayFieldName="true"
                                        v-on="$listeners"
                                        :dbpath="'parser_data.ELFParser.version_info.' + verinfo + '.offset'"
                                    />
                                </td>
                                <td width="33%">
                                    <FilterDropDownMenu
                                        :field="'Addr'"
                                        :value="item.version_info[verinfo].addr != null ? item.version_info[verinfo].addr : 'None'"
                                        :displayFieldName="true"
                                        v-on="$listeners"
                                        :dbpath="'parser_data.ELFParser.version_info.' + verinfo + '.addr'"
                                    />
                                </td>
                            </tr>
                        </table>
                        <b-card
                            v-if="item.version_info[verinfo].entries != null"
                            bg-variant="info"
                            text-variant="white"
                            :header="' Entries for (' + verinfo + ')'"
                            no-body>
                            <div v-if="item.version_info[verinfo].entries != null">
                                <div v-for="(entries, key) in item.version_info[verinfo].entries" :key="key">
                                    <b-card 
                                        bg-variant="info"
                                        text-variant="white"
                                        :header="' Entry Name (' + entries.name + ')'"
                                        no-body>
                                        <table class="general">
                                            <tbody>
                                                <tr>
                                                    <td width="50%">
                                                        <FilterDropDownMenu
                                                            :field="'VN Version'"
                                                            :value="entries.entry.vn_version"
                                                            :displayFieldName="true"
                                                            v-on="$listeners"
                                                            :dbpath="'parser_data.ELFParser.version_info.' + verinfo + '.entries.entry.vn_version'"
                                                        />
                                                    </td>
                                                    <td width="50%">
                                                        <FilterDropDownMenu
                                                            :field="'VN CNT'"
                                                            :value="entries.entry.vn_cnt"
                                                            :displayFieldName="true"
                                                            v-on="$listeners"
                                                            :dbpath="'parser_data.ELFParser.version_info.' + verinfo + '.entries.entry.vn_cnt'"
                                                        />
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td width="50%">
                                                        <FilterDropDownMenu
                                                            :field="'VN File'"
                                                            :value="entries.entry.vn_file"
                                                            :displayFieldName="true"
                                                            v-on="$listeners"
                                                            :dbpath="'parser_data.ELFParser.version_info.' + verinfo + '.entries.entry.vn_file'"
                                                        />
                                                    </td>
                                                    <td width="50%">
                                                        <FilterDropDownMenu
                                                            :field="'VN AUX'"
                                                            :value="entries.entry.vn_aux"
                                                            :displayFieldName="true"
                                                            v-on="$listeners"
                                                            :dbpath="'parser_data.ELFParser.version_info.' + verinfo + '.entries.entry.vn_aux'"
                                                        />
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td width="50%">
                                                        <FilterDropDownMenu
                                                            :field="'VN Next'"
                                                            :value="entries.entry.vn_next"
                                                            :displayFieldName="true"
                                                            v-on="$listeners"
                                                            :dbpath="'parser_data.ELFParser.version_info.' + verinfo + '.entries.entry.vn_next'"
                                                        />
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                        
                                        <div v-for="(entry, key) in entries.vernaux" :key="key">
                                            <p class="card-header"> {{ entry.name }}</p>
                                            <FilterTable v-on="$listeners" :items="[entry.entry]" :fields="Object.keys(entry.entry)" :leading="'parser_data.ELFParser.version_info.' + verinfo + '.entries.vernaux.entry.'"/>
                                        </div>
                                    </b-card>
                                </div>
                            </div>
                        </b-card>
                        <b-card
                            v-if="item.version_info[verinfo].symbols != null"
                            bg-variant="info"
                            text-variant="white"
                            :header="' Symbols for (' + verinfo + ')'"
                            no-body>
                            <div v-for="(imp, key) in getKeyFromList(item.version_info[verinfo].symbols)" :key="key">
                                <p class="card-header"> {{ imp }}</p>
                                <FilterTable v-on="$listeners" :items="item.version_info[verinfo].symbols" :fields="getKeyFromList(item.version_info[verinfo].symbols)" :leading="'parser_data.ELFParser.program_headers.' + verinfo + '.symbols.' + imp" :searchInList="true"/>
                            </div>
                        </b-card>
                     </div>
                </b-card>
            </div>
            <!-- #endregion Version Info End -->
            
             <!-- #region Program Headers --> 
            <div v-if="item.program_headers !== null">
                <div v-if="item.program_headers.segments !== null">
                    <br/>
                    <br/>
                    <b-card
                        bg-variant="secondary"
                        text-variant="white"
                        header="Program Header Segments"
                        no-body
                    >
                        <div v-for="(imp, key) in getKeys(item.program_headers.segments)" :key="key">
                            <p class="card-header"> {{ imp }}</p>
                            <FilterTable v-on="$listeners" :items="item.program_headers.segments[imp]" :fields="getKeyFromList(item.program_headers.segments[imp])" :leading="'parser_data.ELFParser.program_headers.segments.' + imp + '.'"/>
                        </div>
                    </b-card>
                </div>
            </div>
                
            <div v-if="item.program_headers !== null">
                <div v-if="item.program_headers.sections !== null">
                    <br/>
                    <br/>
                    <b-card
                        bg-variant="secondary"
                        text-variant="white"
                        header="Program Header Sections"
                        no-body
                    >
                        <div v-for="(imp, key) in this.getKeys(item.program_headers.sections)" :key="key">
                            <p class="card-header"> {{ imp }}</p>
                            <FilterTable v-on="$listeners" :items="item.program_headers.sections[imp]" :fields="getKeyFromList(item.program_headers.sections[imp])" :leading="'parser_data.ELFParser.program_headers.sections.' + imp + '.'"/>
                        </div>
                    </b-card>
                </div>
            </div>
            <!-- #endregion Program Headers End --> 

            <!-- #region Section Headers --> 
            <div v-if="item.section_headers !== null" :key="'elfparser_section_header'">
                <br/>
                <br/>
                <b-card
                    bg-variant="info"
                    text-variant="white"
                    header="Sections Header Table(s)"
                    no-body
                >
                    <FilterTable
                        v-on="$listeners"
                        :items="item.section_headers"
                        :fields="getKeyFromList(item.section_headers)"
                        leading="parser_data.ELFParser.section_headers."
                    />
                </b-card>
            </div>
            <!-- #endregion Section Headers End --> 

            <!-- #region Dynamic Tags -->
            <div v-if="item.dynamic_tags.length !== 0" :key="'elfparser_dynamic_tags'">
                <br/>
                <br/>
                <b-card
                    bg-variant="secondary"
                    text-variant="white"
                    header="Dynamic Tags"
                    no-body
                >
                    <FilterTable
                        v-on="$listeners"
                        :items="item.dynamic_tags"
                        :fields="getKeyFromList(item.dynamic_tags)"
                        leading="parser_data.ELFParser.dynamic_tags."
                    />
                </b-card>
            </div>
            <!-- #endregion Dynamic Tags -->

            <!-- #region Relocation Data --> 
            <div v-if="item.relocation_data !== null" :key="'elfparser_relocation_data'">
                <br/>
                <br/>
                <b-card
                    bg-variant="secondary"
                    text-variant="white"
                    header="Relocation Data"
                    no-body
                >
                    <FilterTable
                        v-on="$listeners"
                        :items="item.relocation_data"
                        :fields="getKeyFromList(item.relocation_data)"
                        leading="parser_data.ELFParser.relocation_data."
                    />
                </b-card>
            </div>
            <!-- #endregion Relocation Data End -->

            <!-- #region Notes --> 
            <div v-if="item.notes !== null" :key="'elfparser_notes'">
                <br/>
                <br/>
                <b-card
                    bg-variant="info"
                    text-variant="white"
                    header="Notes"
                    no-body
                >
                    <FilterTable
                        v-on="$listeners"
                        :items="item.notes"
                        :fields="getKeyFromList(item.notes)"
                        leading="parser_data.ELFParser.notes."
                    />
                </b-card>
            </div>
            <!-- #endregion Notes End -->

            <!-- #region Architecture Specific Information -->
            <div v-if="item.arch_specific !== null" :key="'elfparser_arch_information'">
                <br/>
                <br/>
                <b-card
                    bg-variant="secondary"
                    text-variant="white"
                    header="Architecture Information"
                    no-body
                >
                    <div v-for="(imp, key) in this.getKeys(item.arch_specific)" :key="key">
                        <div v-for="(data, key1) in item.arch_specific[imp]" :key="key1">
                            <p class="card-header"> {{ imp }} - ( {{data.tag}} )</p> 
                            <FilterTable
                                v-on="$listeners"
                                :items="data.attributes"
                                :fields="getKeyFromList(data.attributes)"
                                :leading="'parser_data.ELFParser.arch_specific.' + imp + '.attributes.'"
                            />
                        </div>
                    </div>
                </b-card>
            </div>
            <!-- #endregion Architecture Specific Information End -->

            <!-- #region Arm Unwind Information --> 
            <div v-if="item.arm_unwind_info != null">
                <br/>
                <br/>
                <b-card
                    bg-variant="secondary"
                    text-variant="white"
                    header="Arm Unwind"
                    no-body
                >
                    <div v-for="(armunwind, key) in this.getKeys(item.arm_unwind_info)" :key="key">
                        <br/>
                        <b-card
                            bg-variant="secondary"
                            text-variant="white"
                            :header=armunwind
                            no-body
                        >

                            <table class="general">
                                <tr>
                                    <td width="33%">
                                        <FilterDropDownMenu
                                            :field="'Original Name'"
                                            :value="item.arm_unwind_info[armunwind].overview.name"
                                            :displayFieldName="true"
                                            v-on="$listeners"
                                            :dbpath="'parser_data.ELFParser.arm_unwind_info.' + armunwind + '.overview.name'"
                                        />
                                    </td>
                                    <td width="33%">
                                        <FilterDropDownMenu
                                            :field="'Off Set'"
                                            :value="item.arm_unwind_info[armunwind].overview.offset"
                                            :displayFieldName="true"
                                            v-on="$listeners"
                                            :dbpath="'parser_data.ELFParser.arm_unwind_info.' + armunwind + '.overview.offset'"
                                        />
                                    </td>
                                    <td width="33%">
                                        <FilterDropDownMenu
                                            :field="'Entry Count'"
                                            :value="item.arm_unwind_info[armunwind].overview.count"
                                            :displayFieldName="true"
                                            v-on="$listeners"
                                            :dbpath="'parser_data.ELFParser.arm_unwind_info.' + armunwind + '.overview.count'"
                                        />
                                    </td>
                                </tr>
                            </table>
                            
                        </b-card>
                    </div>
                </b-card>
            </div>

            <!-- #endregion Arm Unwind Information End --> 
        </b-card>
    </div>
</template>

<script>
import FilterDropDownMenu from "../utils/dropdown/FilterDropDownMenu.vue";
import FilterTable from "../utils/filterTable/FilterTable.vue";
import * as Helpers from "../utils/helpers/Helpers";

export default {
    name: "elfparser_view",
    components: { 
        FilterDropDownMenu,
        FilterTable
    },
    computed: {
        hasError() {
            return this.containsKey(this.item, 'ERROR');
        }
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
}
</script>
