import Vue from 'vue'
import App from './App.vue'
import VueCytoscape from 'vue-cytoscape'
import vuetify from './plugins/vuetify'

Vue.config.productionTip = false

Vue.use(VueCytoscape)

new Vue({
  vuetify,
  render: h => h(App)
}).$mount('#app')
