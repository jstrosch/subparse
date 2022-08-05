<template>
    <span class="field cursor-pointer">
        <a @click="toggleDropdown"
            class="value">
            <span class="all-copy">
              <strong v-if="displayFieldName">{{field}}:</strong> {{value}}</span><span class="fa fa-caret-down"></span>
        </a>
        <div v-if="isOpen"
            class="session-field-dropdown">
                <!-- and --> 
                <b-dropdown-item @click.prevent.stop="add_filter(' == ',  value, '&&')"><strong>and</strong> {{ value }}</b-dropdown-item>
                <!-- and not --> 
                <b-dropdown-item @click.prevent.stop="add_filter(' != ', value, '&&')"><strong>and not</strong> {{ value }}</b-dropdown-item>
                <!-- or --> 
                <b-dropdown-item @click.prevent.stop="add_filter(' == ', value, '||')"><strong>or </strong> {{ value }}</b-dropdown-item>            
                <!-- or not --> 
                <b-dropdown-item @click.prevent.stop="add_filter(' != ', value, '||')"><strong>or not</strong> {{ value }}</b-dropdown-item>
        </div>
    </span>
</template>

<script>

export default {
  name: 'FilterDropDownMenu',
  props: {
    /**
     * Field/Leading text before the dropdown
     */
    field: {
      type: String,
      default: "",
      required: false
    },
    /**
     * Value to be used in the dropdown
     */
    value: {
      type: [String, Number, Boolean],
      default: "",
      required: true
    },
    /**
     * Should the leading text be shown
     */
    displayFieldName: {
      type: Boolean,
      default: false,
      required: false
    },
    /**
     * Path to database for the value
     */
    dbpath: {
      type: String,
      default: "",
      required: true
    },
  },
  methods: {
    /**
     * Adds the filter to the Elasticsearch Query
     */
    add_filter: function(operator, value, type) {
        this.isOpen = false;
        this.$emit('add_filter', (this.dbpath + operator + value), type);
    },
    /**
     * Opens/Closes the dropdown
     */
    toggleDropdown: function () {
        this.isOpen = !this.isOpen;
    },
  },
  data: function () {
    return {
      isOpen: false,
      menuItems: {},
      asyncMenuItems: {},
      molochClickables: undefined,
      menuItemTimeout: null
    };
  }
};
</script>

<style scoped>
@import url("https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css");
.detail-field .field {
  margin: 0 -6px -2px 2px;
  padding: 2px;
}

.detail-field .field a {
  color: var(--color-foreground-accent);
  word-break: break-word;
}

.field {
  position: relative;
  cursor: pointer;
  z-index: 1;
  display: inline-block;
  padding: 0 1px;
  /* margin: 0 -4px 0 0; */
  border-radius: 3px;
  border: 1px solid transparent;
  /* max-width: 98%; */
  line-height: 1.3;
}

/* .field:not(.time-field) {
  word-break: break-all;
} */

.field a {
  color: var(--color-foreground-accent);
  text-decoration: none;
}

.field a .fa {
  opacity: 0;
  visibility: hidden;
  margin-left: var(--px-xs);
}

.field.time-field {
  display: inline-block;
  margin-right: 6px;
}

.field:hover {
  z-index: 4;
  background-color: var(--color-white);
  /* border: 1px solid var(--color-gray-light); */
}

.field:hover a {
  color: var(--color-black);
}

/* if a user right clicks a value, highlight the entire value */
.field a .all-copy {
  -webkit-user-select: all;
     -moz-user-select: all;
      -ms-user-select: all;
          user-select: all;
}

.field:hover ul.session-field-dropdown {
  opacity: 1;
  visibility: visible;
}

.field:hover .fa {
  opacity: 1;
  visibility: visible;
}

.field-children:not(:first-child) {
  margin-top: -3px;
}

/* custom session field dropdown styles because we can't use the dropdown-menu
 * class as it is specific to bootstraps dropdown implementation
 * this class is the same as dropdown-menu, but LESS whitespace */
.session-field-dropdown {
  font-size: 12px;
  position: absolute;
  opacity: 0;
  visibility: hidden;
  max-width: 700px;
  min-width: 160px;
  max-height: 300px;
  overflow-y: auto;
  position: absolute;
  z-index: 1000;
  display: block;
  padding: 5px 0;
  text-align: left;
  list-style: none;
  border-radius: 4px;
  background-color: #a6a6a6;
  border: 1px solid var(--color-gray-light);
  margin-top: 0;
  margin-left: -2px;

          background-clip: padding-box;
  -webkit-background-clip: padding-box;

          box-shadow: 0 6px 12px -3px #333;
  -webkit-box-shadow: 0 6px 12px -3px #333;
}

.field:hover .session-field-dropdown {
  opacity: 1;
  visibility: visible;;
}

.session-field-dropdown.pull-right {
  right: 0;
  left: auto;
}
.session-field-dropdown.pull-left {
  left: 0;
  right: auto;
}
</style>

<style>
.session-field-dropdown a.dropdown-item {
  overflow: hidden;
  text-overflow: ellipsis;
  display: block;
  padding: 2px 8px;
  clear: both;
  font-weight: normal;
  line-height: 1.42857143;
  color: var(--color-foreground, #212529);
  white-space: nowrap;
}

.session-field-dropdown a.dropdown-item:hover {
  text-decoration: none;
  color: var(--color-black);
  background-color: var(--color-gray-lighter);
}
</style>
