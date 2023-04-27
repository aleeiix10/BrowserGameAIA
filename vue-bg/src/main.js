import { createApp, ref } from 'vue'
// Importamos el componente HelloDjango
import HelloDjango from './components/HelloDjango'

// Creamos una instancia de la aplicación Vue
const app = createApp({
  // Elemento html donde se va ha renderizar el contenido
  el: '#app',
  // Cambiamos los delimiters de las variables para que sean diferentes a los de Django
  delimiters: ['[[', ']]'],
  // Activamos el componente dentro de la app
  components : {
    HelloDjango
  },
  // Creamos variable msg reactiva con ref
  data () {
    return {
      msg: ref('Componente de VueJS 3')
    }
  },
})
// Montamos la app en el div #app de nuestra plantilla index.html.
app.mount('#app')