<template>
  <div class="ps-1 pt-1 pe-1 pb-1">
    <div class="mb-1" v-on-clickaway="onOffFocus">
      <!-- Start of Input/Buttons for searching -->
      <div class="input-group input-group-sm">
        <b-form-input
          ref="searchbar"
          v-bind:value="searchQuery"
          autocomplete="off"
          placeholder="Search"
          v-on:focus.native="onFocus"
          v-on:input="inputChanged($event)"
          @keydown.esc="escPressed"
          @keydown.enter="enterEvent()"
          @keydown.down.up="arrowEvent($event)"
        />
        <span class="input-group-append ps-1">
          <button
            type="button"
            @click="search()"
            class="btn btn-clear-input btn-outline-secondary"
          >
            <span class="fa fa-search"> </span>
          </button>
        </span>
        <span class="input-group-append ps-1">
          <button
            type="button"
            @click="clear_search()"
            class="btn btn-outline-secondary btn-clear-input"
          >
            <span class="fa fa-close"> </span>
          </button>
        </span>
      </div>
      <!-- End of Input/Buttons for searching -->

      <!-- Start of results dropdown -->
      <div
        id="typeahead-results"
        ref="typeaheadResults"
        class="dropdown-menu typeahead-results"
        v-show="th_results.length && focusInput"
      >
        <template v-for="(value, key) in th_results">
          <a :id="key+'_item'"
            :key="key+'_item'"
            @click="addToQuery(value)"
            class="dropdown-item cursor-pointer"
            @keydown.enter="[selectedDDCount != key ? null : addToQuery(value)]"
            v-bind:style="[selectedDDCount != key ? {'background': '#a6a6a6'} : {'background': '#212529'}]">
            <strong v-if="!value.exp">{{ value }}</strong>
            
          </a>
        </template>
      </div>
      <!-- End of results dropdown -->
    </div>
  </div>
</template>

<script>
import { mixin as clickaway } from 'vue-clickaway';

export default {
  name: "Search",
  mixins: [clickaway],
  compontents: {},
  data: function () {
    return {
      filterError: false,
      focusInput: false,
      selectedDDCount: -1
    };
  },
  watch: {
    /**
     * This watches for the input change on the search box so that it can handle showing the dropdown menu
     */
    focusInput: function() {
      if(!this.focusInput){
        this.selectedDDCount = -1;
      }
    }
  },
  methods: {
    /**
     * Arrow Event Handler for navigation in the dropdown typeahead menu
     * 
     * Down Arrow: keycode 40
     * Up Arrow: keycode 38
     */
    arrowEvent: function(event){
      if(event.keyCode == 38){
        if(this.selectedDDCount != -1) {
          this.selectedDDCount--;
        }
      }
      if(event.keyCode == 40){
        this.selectedDDCount++;
      }
    },
    /**
     * Dropdown Enter Key Pressed, this will allow the selected typeahead value 
     *  to be added to the search box / search query
     */
    dropdownEnterKey: function() {
        this.addToQuery(this.th_results.at(this.selectedDDCount));
        this.selectedDDCount = -1;
    },
    /**
     * Handles and determines which Enter event is suppose to be used
     *  if the dropdown menu is visable or not
     */
    enterEvent: function(){
      if(this.selectedDDCount == -1){
        this.search(); 
      }else{
        this.dropdownEnterKey();
      }
    },
    /**
     * Event handler for if the input has changed in the search text box 
     *  which is attached the the query variable
     */
    inputChanged: function(event) { 
      this.$emit('update:searchQuery', event);
      this.focusInput = true;
    },
    /**
     * Escape button event handler
     *  will change focus or hide the dropdown menu depending on the current state of the page
     */
    escPressed: function() {
      if(this.selectedDDCount != -1 || this.focusInput == true) {
      this.focusInput = false;
      this.selectedDDCount = -1;
      }else{
        this.$refs.searchbar.$el.blur(); 
      }
    },
    /**
     * Clear button event handler 
     *  emits a clear event to the parent view
     */
    clear_search: function () {
      this.$emit("search_reset_event");
    },
    /**
     * Search button event handler
     *  emits a search event for the parent view
     */
    search: function () {
      this.$emit("search_event");
    },
    /**
     * Off switch function for input focus
     */
    onOffFocus: function() { 
      this.focusInput = false;
    },
    /**
     * On switch function for input focus
     */
    onFocus: function() {
      this.focusInput = true;
    },
    /**
     * Emits an event for adding suggestions for the search query
     */
    addToQuery: function(val){
      this.$emit("added_from_suggestion", val);
      this.focusInput = true;
    }
  },
  props: {
    searchQuery: String,
    th_results: Array,
  },
};
</script>

<style scoped>
.v-select {
  display: grid;
}
.btn:focus {
  outline: none;
  box-shadow: none;
}

/* make sure the width of the input prepend doesn't change */
.input-group-prepend-fw,
.input-group-text-fw {
  width: 36px;
}

.input-group {
  flex-wrap: none;
  width: auto;
}

.typeahead-results {
  top: initial;
  left: initial;
  display: block;
  overflow-y: auto;
  overflow-x: hidden;
  max-height: 500px;
  margin-left: 35px;
}

.typeahead-results a.last-history-item {
  border-bottom: 1px solid var(--color-gray);
}

@media screen and (max-height: 600px) {
  .typeahead-results {
    max-height: 250px;
  }
}
</style>
