import Vue from 'vue';
import App from "@/App";
import router from "@/router";

import {
  BootstrapVue,
  IconsPlugin,
  LayoutPlugin,
  CardPlugin,
  DropdownPlugin,
  TablePlugin,
  ModalPlugin,
} from "bootstrap-vue";
import { Plugin as Fragment } from "vue-fragment";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";
import './themes/overrides.css';
// import './themes/subparse-light.css';
import './themes/subparse-dark.css';

Vue.use(BootstrapVue);
Vue.use(ModalPlugin);
Vue.use(LayoutPlugin);
Vue.use(CardPlugin);
Vue.use(IconsPlugin);
Vue.use(DropdownPlugin);
Vue.use(TablePlugin);
Vue.use(Fragment);

Vue.config.productionTip = false;

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  render: (h) => h(App),
  created: function () {
    // define app constants
    /* eslint-disable no-undef */
    Vue.prototype.$constants = {

    };
  }
});