import {createApp} from 'vue'
import PaginadorComponent from './components/PaginadorComponent.vue'
import consoleEvent from './components/ConsoleEvent.vue'

// Montamos la app en el div #app de nuestra plantilla index.html.
createApp(PaginadorComponent).mount('#app')
createApp(consoleEvent).mount("#modalVue")