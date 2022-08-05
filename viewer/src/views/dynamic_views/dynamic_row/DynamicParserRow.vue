<template>
    <div>
        <div v-for="(componentName, index) in supportedComponents" :key="index">
            <br/>
            <component v-if="item.parser_data[componentName] !== null && Object.keys(item.parser_data[componentName]) !== 0" :is="componentName" v-on="$listeners" v-bind:item="item.parser_data[componentName]"></component>
        </div>
    </div>
</template>

<script>
    export default {
        name: "DynamicParserRow",
        props: {
            /**
             * Dynamic parser view data
             */
            item: {
                type: Object,
                required: true,
            },
            /**
             * List of other components that are needed for the parser
             */
            supportedComponents: {
                type: Array,
                required: true
            }
        },
        created ()  {
            
            for(let c=0; c<this.supportedComponents.length; c++) {
                let componentName = this.supportedComponents[c];
                this.$options.components[componentName] = () => import("../../parser_views/" + componentName.toLowerCase().trim() + '_view.vue');
            }
        }
    };
</script>