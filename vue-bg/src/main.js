import { createApp} from 'vue'
// Importamos el componente HelloDjango
// import HelloDjango from './components/HelloDjango'

// Creamos una instancia de la aplicación Vue
const app = createApp({
  // Elemento html donde se va ha renderizar el contenido
  el: '#app',
  // Cambiamos los delimiters de las variables para que sean diferentes a los de Django
  delimiters: ['[[', ']]'],
  // Activamos el componente dentro de la app
  // components : {
  //   HelloDjango
  // },
  // Creamos variable msg reactiva con ref
  data(){
    return {
      arrayUsers: [],
      elementsByPage: 2,
      dataPage: [],
      currentPage: 1
    }
  },
  mounted() {
    fetch('/get_user')
      .then(response => {
        return response.json();
      })
      .then(data => {
        console.log(data)
        this.arrayUsers = data.users;
        this.getDataPage(1)
      })
      .catch(error => {
        console.log(error);
      })
  },
  methods:{
    totalPages(){
      return Math.ceil(this.arrayUsers.length/this.elementsByPage)
    },
    getDataPage(numPage){
      this.currentPage= numPage
      this.dataPage= []
      let ini= (numPage * this.elementsByPage) - this.elementsByPage
      let end= (numPage * this.elementsByPage)
      this.dataPage= this.arrayUsers.slice(ini,end)
      console.log(this.dataPage)
    },
    getPreviusPage(){
      if(this.currentPage > 1){
        this.currentPage--
      }
      this.getDataPage(this.currentPage)
    },
    getNextPage(){
      if(this.currentPage < this.totalPages()){
        this.currentPage++
      }
      this.getDataPage(this.currentPage)
    },
    isActive(numPage){
      if(numPage==this.currentPage){
        return('bg-green-600')
      }
      else{
        return('')
      }
    }
  }
})
// Montamos la app en el div #app de nuestra plantilla index.html.
app.mount('#app')