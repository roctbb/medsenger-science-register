import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"
import {createApp} from 'vue'
import {library} from '@fortawesome/fontawesome-svg-core'
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome'
import {faCircleXmark} from '@fortawesome/free-regular-svg-icons'
import {faPen} from '@fortawesome/free-solid-svg-icons'
import {faTimes} from '@fortawesome/free-solid-svg-icons'
import App from './App.vue'
import helpersPlugin from "@/plugins/helpers";
import applicationPlugin from "@/plugins/application";
import router from '@/router'

library.add(faCircleXmark, faPen, faTimes)

const app = createApp(App)
app.component('font-awesome-icon', FontAwesomeIcon)
app.use(helpersPlugin)
app.use(applicationPlugin)
app.use(router)

app.mount('#app')



