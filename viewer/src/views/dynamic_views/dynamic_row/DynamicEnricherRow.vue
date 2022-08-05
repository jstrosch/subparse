<template>
    <div>
        <div v-for="(componentName, index) in supportedComponents" :key="index">
            <br/>
            
            <component v-if="item.enricher_data[componentName] !== null && Object.keys(item.enricher_data[componentName]).length !== 0" :is="componentName" v-on="$listeners" v-bind:item="item.enricher_data[componentName]"></component>
        </div>
    </div>
</template>

<script>
    export default {
        name: "DynamicEnricherRow",
        props: {
            /**
             * Dynamic enricher view data
             */
            item: {
                type: Object,
                required: true,
            },
            /**
             * List of other components that are needed for the enricher
             */
            supportedComponents: {
                type: Array,
                required: true
            }
        },
        created ()  {
            for(let c=0; c<this.supportedComponents.length; c++) {
                let componentName = this.supportedComponents[c];
                this.$options.components[componentName] = () => import("../../enricher_views/" + componentName.toLowerCase().trim() + '_view.vue');
            }
        }
    };
</script>