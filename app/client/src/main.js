import Vue from 'vue'
import App from './App.vue'
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css'
import 'vue-search-select/dist/VueSearchSelect.css'

import BootstrapVue from 'bootstrap-vue';
import VueProgressBar from 'vue-progressbar'
import axios from 'axios'
import VueAxios from 'vue-axios'
import HighchartsVue from 'highcharts-vue'
Vue.use(HighchartsVue)


Vue.config.productionTip = false
 
Vue.use(BootstrapVue);
Vue.use(VueAxios, axios)
Vue.use(VueProgressBar, {
  color: 'blue',
  failedColor: 'red',
  height: '10px'
})

new Vue({
  render: h => h(App),
}).$mount('#app')
