<template>
  <div>
    <b-card bg-variant="subparse-default" text-variant="white" header="General Info" no-body>  
        <br />    
        <table class="general">
            <tbody>
                <tr>
                    <td width="30%">
                        <FilterDropDownMenu :field="'Updated On'" :value="converttime(item.updated_on)" :displayFieldName="true" v-on="$listeners" :dbpath="'updated_on'"/>
                    </td>
                </tr>
                <br/>
                <tr>
                    <td width="20%">
                    <FilterDropDownMenu :field="'MD5'" :value="item.md5" :displayFieldName="true" v-on="$listeners" :dbpath="'md5'"/>
                    </td>
                    
                    <td width="50%">
                    <FilterDropDownMenu :field="'File Magic'" :value="item.file_magic" :displayFieldName="true" v-on="$listeners" :dbpath="'file_magic'"/>
                    </td>
                </tr>
            </tbody>
        </table>
        <br />
    </b-card>
  </div>
</template>

<script>
    import FilterDropDownMenu from "../../utils/dropdown/FilterDropDownMenu.vue";
    
    export default {
        name: "GeneralInfoRow",
        components: {
            FilterDropDownMenu
        },
        props: {
            /**
             * Elasticsearch general information data
             */
            item: {
                type: Object,
                required: true,
            }
        },
        methods: {
            /**
             * Convert time stamp to a better format for the table
             */
            converttime: function (datetime){
                const current = new Date(datetime);
                const date = (current.getMonth()+1)+'/'+current.getDate()+'/'+current.getFullYear();
                const time = current.getHours() + ":" + current.getMinutes() + ":" + current.getSeconds();
                const dateTime = date +' '+ time;
                return dateTime;
            },    
        }
    };
</script>