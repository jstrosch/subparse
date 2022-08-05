# SubParse - VUE
This viewer can be used to view and search any files parsed into the elasticsearch database used by the parser. The following commands can be used to get it up and running, as well as fix certain issues.

## Installation
---
Before running the viewer, it needs to be installed with the following command:
```
$ npm install
```

### Compiling and Reloading
After installation, this command starts a development version of the site:
```
$ npm run serve
```

### Compiling and Minifying for Production
This command compiles the project into an executable [TODO: Double check this. I have no experience with this command.]
```
$ npm run build
```

### Linting and Fixing Files
For development purposes, this command can be used to identify issues in the code of the viewer:
```
$ npm run lint
```

### Customize Configuration
To customize the configuration of the vapp, see [Configuration Reference](https://cli.vuejs.org/config/).
<p>&nbsp;</p>

## Development 
---

Below is examples of develping the Vue side for both parsers and enrichers. These can be used as 'templates' to develop your own custom Vue for the corresponding module.

### General Requirements
---
There are some basic requirements that all of the parser/enrichers will need to follow to allow them to be used by the program.

<details>
<summary>Filename</summary>
</br>
Regardless, if you are making an enricher or a parser the general filename will be the same. Please make sure that the filename is lower cased, otherwise the program will not use it.

* testparser_view.vue
* testenricher_view.vue

</details>

<details>
<summary>Class Name</summary>
</br>
In the export default section of your vue page, there is parameter called name. This parameter needs to match the filename of the page. Below are two examples that match the filename examples shown above.

* testparser_view
* testenricher_view

</details>
<p>&nbsp;</p>
</br>

### Parser Example
---
Below is a template for developing the Vue.js file that is needed when building out a custom parser module.

General file information: 
* Location to place the Vue.js file within the framework: subparse/viewer/src/views/parser_views
* File naming schema: [parser name]parser_view.vue

There are a few things that you need to change when implementing your version of the template:

| Location | Change | Reason |
| ----------- | ----------- | ----------- |
| header="Test Parser" | header="[Your Parser Name] Parser" | The header is used on your custom card template to allow for seperation in the HTML that gets generated and for debugging |
| name: "testparser_view" | name: "[Your Parser Name]parser_view" | This needs to be ALL lowercase following the alt example, this allows us to dynamically call your template for showing the data |

Note: Props for the template ```SHOULD NOT``` be altered! The item prop is used to pass along the actual data from our framework into your custom template, the item prop will hold the reference to the Elasticsearch data for the template. Other default attributes such as components and other Vue.js fields in the export default section can still be added to your template without any concerns, just nothing to do with modification of the props.

</br>
<details>
<summary>Parser Template Example</summary>
</br>

```js
<template>
    <!-- #region Error -->
    <div v-if="hasError">
        <h1>ERROR</h1>
    </div>
    <!-- #endregion Error End-->
    <div v-else>
         <div> 
            <b-card bg-variant="subparse-default" text-variant="white" header="Test Parser" no-body>  
                <p> Testing Parser </p>
            </b-card>
        </div>
    </div>
</template>

<script>
export default {
    name: "testparser_view",
    },
    computed: {
        hasError() {
            return this.containsKey(this.item, 'ERROR');
        }
    },
    props: {
        /**
        * Parser Item
        */
        item: {
            type: Object,
            required: true,
        },
    }
}
</script>

```
</details>

</br>
</br>

### Enricher Example
---
Below is a template for developing the Vue.js file that is needed when building out a custom parser module.

General file information: 
* Location to place the Vue.js file within the framework: subparse/viewer/src/views/enricher_views
* File naming schema: [enricher name]enricher_view.vue

Note: Filename should be ALL lowercase

There are a few things that you need to change when implementing your version of the template:

| Location | Change | Reason |
| ----------- | ----------- | ----------- |
| header="Rest Enricher" | header="[Your Enricher] Enricher" | The header is used on your custom card template to allow for seperation in the HTML that gets generated and for debugging |
| "testenricher_view" | "[Your Enricher]enricher_view" | This needs to be ALL lowercase following the abuse example, this allows us to dynamically call your template for showing the data |


Note: Props for the template ```SHOULD NOT``` be altered! The item prop is used to pass along the actual data from our framework into your custom template, the item prop will hold the reference to the Elasticsearch data for the template. Other default attributes such as components and other Vue.js fields in the export default section can still be added to your template without any concerns, just nothing to do with modification of the props.

</br>
<details>
<summary>Enricher Template Example</summary>
</br>

```js
<template>
    <!-- #region Error -->
    <div v-if="hasError">
        <h1>ERROR</h1>
    </div>
    <!-- #endregion Error End-->
    <div v-else>
         <div> 
            <b-card bg-variant="subparse-default" text-variant="white" header="Test Enricher" no-body>  
                <p> Testing Enricher </p>
            </b-card>
        </div>
    </div>
</template>

<script>
export default {
    name: "testenricher_view",
    computed: {
        hasError() {
            return this.containsKey(this.item, 'ERROR');
        }
    },
    props: {
        /**
        * Enricher Item
        */
        item: {
            type: Object,
            required: true,
        },
    }
}
</script>

```
</details>
