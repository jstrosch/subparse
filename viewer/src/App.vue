<template>
  <div id="app">
    <!-- <p>Test</p> -->
    <subparse-navbar/>
    <keep-alive>
      <router-view/>
    </keep-alive>
  </div>
</template>

<script>
import SubparseNavbar from './views/utils/Navbar.vue';

export default {
  name: 'App',
  components: {
    SubparseNavbar
  }
}
</script>

<style>
/* styles for bottom footer */
html {
  position: relative;
  min-height: 100%;
}
#app {
  padding-bottom: 25px;
}

body {
  /* color: var(--color-foreground); */
  background-color: var(--color-background);
}


/* text */
.text-theme-accent    { color: var(--color-foreground-accent); }
.text-theme-primary   { color: var(--color-primary); }
.text-theme-secondary { color: var(--color-secondary); }
.text-theme-tertiary  { color: var(--color-tertiary); }
.text-theme-quaternary{ color: var(--color-quaternary); }
.text-muted-more      { color: var(--color-gray); }
.text-theme-white     { color: var(--color-white); }
.text-theme-button    { color: var(--color-button, #FFF); }

.text-theme-gray-hover:hover {
  color: var(--color-gray);
}

/* displaying */
.fixed-header {
  z-index: 5;
  position: fixed;
  left: 0;
  right: 0;
  background-color: var(--color-quaternary-lightest);

  -webkit-box-shadow: 0 0 16px -2px black;
     -moz-box-shadow: 0 0 16px -2px black;
          box-shadow: 0 0 16px -2px black;
}

/* themed buttons */
a[class*=' btn-theme'],
div[class*=' btn-theme'],
button[class*=' btn-theme'] {
  color: var(--color-button, #FFF) !important;
}

.btn-clear-input {
  color: var(--color-foreground, #555) !important;
  background-color: var(--color-background, #EEE) !important;
  border-color: var(--color-gray) !important;
}

.btn.btn-danger,
.btn.btn-primary,
.btn.btn-theme-primary {
  color           : var(--color-button, #FFF);
  background-color: var(--color-primary);
  border-color    : var(--color-primary-dark);
}
.btn.btn-danger:hover,
.btn.btn-primary:hover,
.btn.btn-theme-primary:hover {
  background-color: var(--color-primary-dark);
  border-color    : var(--color-primary-darker);
}
.btn.btn-danger.active,
.btn.btn-primary.active,
.btn.btn-theme-primary.active {
  background-color: var(--color-primary-darker);
  border-color    : var(--color-primary-darker);
}

.btn.btn-warning,
.btn.btn-theme-secondary {
  color           : var(--color-button, #FFF);
  background-color: var(--color-secondary);
  border-color    : var(--color-secondary-dark);
}
.btn.btn-warning:hover,
.btn.btn-theme-secondary:hover {
  background-color: var(--color-secondary-dark);
  border-color    : var(--color-secondary-darker);
}
.btn.btn-warning.active,
.btn.btn-theme-secondary.active {
  background-color: var(--color-secondary-darker);
  border-color    : var(--color-secondary-darker);
}

.btn.btn-success,
.btn.btn-theme-tertiary {
  color           : var(--color-button, #FFF);
  background-color: var(--color-tertiary);
  border-color    : var(--color-tertiary-dark);
}
.btn.btn-success:hover,
.btn.btn-theme-tertiary:hover {
  background-color: var(--color-tertiary-dark);
  border-color    : var(--color-tertiary-darker);
}
.btn.btn-success:active,
.btn.btn-theme-tertiary.active {
  background-color: var(--color-tertiary-darker);
  border-color    : var(--color-tertiary-darker);
}

.btn.btn-info,
.btn.btn-theme-quaternary {
  color           : var(--color-button, #FFF);
  background-color: var(--color-quaternary);
  border-color    : var(--color-quaternary-dark);
}
.btn.btn-info:hover,
.btn.btn-theme-quaternary:hover {
  background-color: var(--color-quaternary-dark);
  border-color    : var(--color-quaternary-darker);
}
.btn.btn-info.active,
.btn.btn-theme-quaternary.active {
  background-color: var(--color-quaternary-darker);
  border-color    : var(--color-quaternary-darker);
}

/* themed radio/checkbox buttons */
label.btn-radio,
button.btn-checkbox,
div.btn-checkbox > label,
div.btn-group-toggle > label {
  cursor: pointer;
  background-image: none;
  background-color: var(--color-background, white) !important;
  border-color    : var(--color-primary) !important;
  color           : var(--color-primary) !important;
}
label.btn-radio.active:hover:not(:disabled),
button.btn-checkbox.active:hover:not(:disabled),
div.btn-checkbox > label.active:hover:not(:disabled) {
  background-color: var(--color-primary-darker) !important;
  color: var(--color-button, #FFF) !important;
}
label.btn-radio:hover:not(:disabled),
button.btn-checkbox:hover:not(:disabled),
div.btn-checkbox > label:hover:not(:disabled) {
  color           : var(--color-primary);
  background-color: var(--color-primary-lightest) !important;
}
label.btn-radio.active:not(:disabled),
button.btn-checkbox.active:not(:disabled),
div.btn-checkbox > label.active:not(:disabled),
.btn-group-checkboxes label.btn-secondary.active:not(:disabled) {
  border-color    : var(--color-primary) !important;
  background-color: var(--color-primary) !important;
  color: var(--color-button, #FFF) !important;
}
label.btn-radio:disabled,
button.btn-checkbox:disabled,
div.btn-checkbox > label:disabled {
  background-color: var(--color-background, white);
  color: var(--color-gray);
  border-color: var(--color-gray) !important;
  cursor: not-allowed;
}

/* themed labels */
.label.label-theme-primary {
  background-color: var(--color-primary);
}
.label.label-theme-secondary {
  background-color: var(--color-secondary);
}
.label.label-theme-tertiary {
  background-color: var(--color-tertiary);
}
.label.label-theme-quaternary {
  background-color: var(--color-quaternary);
}

/* see top level common.css info area for usage */
.info-area { color: var(--color-gray-dark); }
.info-area > div { background-color: var(--color-gray-light); }

/* small alert areas */
.alert.alert-sm {
  padding       : 4px 35px 3px 8px;
  margin-top    : var(--px-none);
  margin-bottom : var(--px-none);
  font-size     : .85rem;
}
.alert.alert-sm button.close {
  padding: 0 .5rem;
}

/* theme alert areas */
.alert.alert-info {
  color: var(--color-primary);
  border-color: var(--color-primary-darkest);
  background-color: var(--color-primary-lightest);
}
.alert.alert-danger {
  color: var(--color-secondary);
  border-color: var(--color-secondary-darkest);
  background-color: var(--color-secondary-lightest);
}
.alert.alert-success {
  color: var(--color-tertiary);
  border-color: var(--color-tertiary-darkest);
  background-color: var(--color-tertiary-lightest);
}
.alert.alert-warning {
  color: var(--color-quaternary);
  border-color: var(--color-quaternary-darkest);
  background-color: var(--color-quaternary-lightest);
}

/* sub navbars */
.sub-navbar {
  position: fixed;
  top: 36px;
  left: 0;
  right: 0;
  padding: var(--px-lg) var(--px-md) var(--px-sm) 13px;
  background-color: var(--color-secondary-lightest);
  -webkit-box-shadow: 0 0 16px -2px black;
     -moz-box-shadow: 0 0 16px -2px black;
          box-shadow: 0 0 16px -2px black;
}
.sub-navbar .sub-navbar-title {
  font-size: 19px;
  font-weight: bold;
}
.sub-navbar .sub-navbar-title .fa-stack {
  margin-top: -14px;
}
.sub-navbar > .toast-container {
  margin-top: -6px;
}

/* description list styles */
dl.dl-horizontal dt {
  float: left;
  width: 190px;
  overflow: hidden;
  clear: left;
  text-align: right;
  text-overflow: ellipsis;
  white-space: nowrap;
  margin-bottom: 0;
}
dl.dl-horizontal dd {
  margin-left: 205px;
  margin-bottom: 0;
}
dl.dl-horizontal.dl-horizontal-wide dt {
  width: 400px;
}
dl.dl-horizontal.dl-horizontal-wide dd {
  margin-left: 410px;
  margin-bottom: 0;
}

/* make the shortcut letter the same size/position as the icon */
.query-shortcut {
  color: var(--color-tertiary-lighter);
  font-size: 14px;
  width: 20px;
}
.time-shortcut {
  color: var(--color-tertiary-lighter);
  font-size: 14px;
  width: 20px;
}
/* make sure the width of the input prepend doesn't change */
.input-group-prepend-fw, .input-group-text-fw {
  width: 36px;
}

/* enter icon for search/refresh button to be displayed on shift hold */
.search-btn { width: 62px; }
.refresh-btn { width: 66px; }
.enter-icon > .fa-long-arrow-left {
  position: relative;
  top: 2px;
}
.enter-icon > .enter-arm {
  display: inline-block;
  height: 9px;
  width: 3px;
  background-color: var(--color-white, #FFFFFF);
  position: relative;
  top: -2px;
  right: 6px;
}

/* custom font awesome icons */
.fa.fa-venn {
  position: relative;
  display: inline-block;
  vertical-align: middle;
  width: 1.28571429em;
  text-align: center;
}
.fa.fa-venn > span.fa-circle-o {
  position: absolute;
  top: -7px;
}
.fa.fa-venn> span.fa-circle-o:first-child {
  left: 5px;
}
.fa.fa-venn> span.fa-circle-o:last-child {
  right: 6px;
}

/* info page (404 & upgrade) */
.moloch-info {
  margin-top: 20px;
}

.moloch-info .center-area > img {
  z-index: 99;
}

.moloch-info .center-area {
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  flex-direction: column;
  min-height: 75vh;
}

.moloch-info .well {
  margin-top: -6px;
  min-width: 25%;
  box-shadow: 4px 4px 10px 0 rgba(0,0,0,0.5);
}

.moloch-info .well > h1 {
  margin-top: 0;
  color: var(--color-primary);
}

/* apply theme foreground to tables */
table.table {
  color: var(--color-foreground, #555);
}

/* column resize grips */
.grip {
  width: 8px;
  top: -2px;
  right: -4px;
  bottom: -2px;
  cursor: col-resize;
  position: absolute;
  z-index: 9;
}

/* badge remove button */
.badge > button.close {
  line-height: 0.4;
  font-size: 1.2rem;
  margin-left: 0.3rem;
}

/* application information error */
.app-info-error {
  right: 10px;
  bottom: 15px;
  z-index: 999;
  position: fixed;
}
.app-info-error > div.alert {
  font-size: 17px;
}
</style>
