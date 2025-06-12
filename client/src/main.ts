import { createApp } from 'vue'
import { createVuestic } from 'vuestic-ui'
import stores from './stores'
import router from './router'
import vuesticGlobalConfig from './services/vuestic-ui/global-config'
import App from './App.vue'
import 'vue-files-preview/lib/style.css'

const app = createApp(App)

app.use(stores)
app.use(router)
app.use(createVuestic({ config: vuesticGlobalConfig }))
app.mount('#app')
