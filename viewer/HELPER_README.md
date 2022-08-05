# SubParse - VUE Helpers : (Built-in Widgets)

## *Filter Table Widget*
---

The FilterTable is a pre-built Bootstrap table that offers cells that are prewrapped with the FilterDropDownMenu ability to help save time when implementing your own custom tables and keeping all of the features that are offered for the usage of data and searchability. 

The first thing that needs to be done is to import the object and add it to the components of the default export, making the script section of the file look something like this:


```js
<script>
import FilterTable from "../utils/filterTable/FilterTable.vue";

export default {
  
  data: function () {
    return {
        ...
    };
  },
  components: {
    FilterTable
  }
  ...
}
</script>
```
Now to add the FilterTable to your view: 

```js
<template>
    <div>
        <b-card ...>
            <FilterTable 
                v-on="$listeners" 
                :items="item.sections" 
                :fields="section_fields" 
                :leading="parser_data.PEParser.sections." />
        </b-card>
    </dvi>
</template>
```

Changes to make for the field that you are trying to use this on:

| Attr | Required | Value |
| ----------- | ----------- | ----------- |
| :items | Yes | This field requires a list of dictionaries where the keys in the dictionary correspond to the column that the value is suppose to reside. See below for a sample of the data expected. |
| :fields | Yes | An array of strings, this will be used for the column header information |
| :leading | Yes | This is the path to where the information can be found in the Elastic database and MUST be prefixed with  |
| v-on | Yes | The value of $listeners should stay in this attribute, this will alert the parent of changes |

Example of expected data for items: 

```json
    [
        {
            "name": "UPX0",
            "virtual_address": "0x1000",
            "virtual_size": "0x36b000",
            "section_raw_size": "0x0",
            "read": true,
            "write": true,
            "execute": true,
            "contains_code": false,
            "contains_init": false,
            "entropy": 0
        },
        {
            "name": "UPX1",
            "virtual_address": "0x36c000",
            "virtual_size": "0x84000",
            "section_raw_size": "0x83400",
            "read": true,
            "write": true,
            "execute": true,
            "contains_code": false,
            "contains_init": true,
            "entropy": 7.904645854087161
        }
    ]
```

<br/>
<br/>

## *Filter Drop Down Menu Widget*
---

The FilterDropDownMenu is used to allow for clickable filter options based on the data the Vue.js view is displaying to the user(s). This allows for users to click on the field and quickly add it to the search field at the top with preset options. This feature is a big bonus to the users and adds a lot of streamlined functionallity to the system including any custom Parsers/Enrichers developed. To implement this feature there are a few changes that you will need to make to the Vue.js file.

The first thing that needs to be done is to import the object and add it to the components of the default export, making the script section of the file look something like this:

```js
<script>
import FilterDropDownMenu from "../utils/dropdown/FilterDropDownMenu.vue";

export default {
  
  data: function () {
    return {
        ...
    };
  },
  components: {
    FilterDropDownMenu
  }
  ...
}
</script>
```

Now to apply the FilterDropDownMenu feature to a field in your template. See below for an example:

```js
<template>
    <div>
        <b-card ...>
            <FilterDropDownMenu
                :field="'Image Base'"
                :value="item.image_base"
                :displayFieldName="true"
                v-on="$listeners"
                :dbpath="'parser_data.PEParser.image_base'"
                />
        </b-card>
    </dvi>
</template>
```

Changes to make for the field that you are trying to use this on:


| Attr | Required | Value |
| ----------- | ----------- | ----------- |
| :field | No | The leading text before the value/drop down |
| :value | Yes | The value that should be in the drop down |
| :displayFieldName | Yes | True/False depending on if you have/want leading text |
| :dbpath | Yes | Full path to the location of the field in the Elastic database, this is how we can do the query building | 
| v-on | Yes | The value of $listeners should stay in this attribute, this will alert the parent of changes | 
