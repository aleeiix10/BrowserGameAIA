<template>
  <main class="container mx-auto my-4">
    <h2 class="text-lg font-semibold mb-2">Ranking Pren Arrels</h2>
    <table class="border border-black">
        <thead class="bg-green-700 text-white">
            <tr>
                <th class="p-2">
                    Nom
                </th>
                <th class="p-2">
                    Nivell
                </th>
                <th class="p-2">
                    Experiència
                </th>
                <th class="p-2">
                    Vida
                </th>
                <th class="p-2">
                    Manà
                </th>
                <th class="p-2">
                    Posició
                </th>
            </tr>
        </thead>
        <tbody>
          <tr v-for="(user, index) in dataPage" :key="index" class="border-b border-black">
                <td class="p-2 text-center">
                  <a :href="`/ranking/${user.username}`">{{user.username}}</a>
                </td>
                <td class="p-2 text-center">
                    {{user.level}}
                </td>
                <td class="p-2 text-center">
                    {{user.experience}}
                </td>
                <td class="p-2 text-center">
                    {{user.current_life}}
                </td>
                <td class="p-2 text-center">
                    {{user.current_mana}}
                </td>
                <td class="p-2 text-center">
                    {{getPosition(index)}}
                </td>
            </tr>
        </tbody>
    </table>
  </main>
  <div class="container mx-auto my-4 flex items-center justify-between border-t border-gray-200 bg-white px-4 py-3 sm:px-6" id="paginator">
    <div class="flex flex-1 justify-between sm:hidden">
      <a href="#" class="relative inline-flex items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50">Previous</a>
      <a href="#" class="relative ml-3 inline-flex items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50">Next</a>
    </div>
    <div class="hidden sm:flex sm:flex-1 sm:items-center sm:justify-between">
      <div>
        <p class="text-sm text-gray-700">
          Mostrant
          <span class="font-medium">{{currentPage}}</span>
          a
          <span class="font-medium">{{totalPages()}}
          </span>
          de
          <span class="font-medium">{{arrayUsers.length}}</span>
          resultats
        </p>
      </div>
        <nav class="isolate inline-flex -space-x-px rounded-md shadow-sm" aria-label="Pagination">
          <a v-on:click="getPreviusPage()" href="#" class="relative inline-flex items-center rounded-l-md px-2 py-2 text-gray-400 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-20 focus:outline-offset-0">
            <span class="sr-only">Previous</span>
            <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
              <path fill-rule="evenodd" d="M12.79 5.23a.75.75 0 01-.02 1.06L8.832 10l3.938 3.71a.75.75 0 11-1.04 1.08l-4.5-4.25a.75.75 0 010-1.08l4.5-4.25a.75.75 0 011.06.02z" clip-rule="evenodd" />
            </svg>
          </a>
          <a v-for="(page) in totalPages()" :key="page" v-on:click="getDataPage(page)" v-bind:class="isActive(page)" href="#" aria-current="page" class="relative inline-flex items-center px-4 py-2 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-gray-300 focus:z-20 focus:outline-offset-0">{{page}}</a>
          <a v-on:click="getNextPage()" href="#" class="relative inline-flex items-center rounded-r-md px-2 py-2 text-gray-400 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-20 focus:outline-offset-0">
            <span class="sr-only">Next</span>
            <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
              <path fill-rule="evenodd" d="M7.21 14.77a.75.75 0 01.02-1.06L11.168 10 7.23 6.29a.75.75 0 111.04-1.08l4.5 4.25a.75.75 0 010 1.08l-4.5 4.25a.75.75 0 01-1.06-.02z" clip-rule="evenodd" />
            </svg>
          </a>
        </nav>
    </div>
  </div>
</template>
<script>
  export default {
    el: '#app',
    name: "PaginadorComponent",
    data() {
      return {
        arrayUsers: [],
        elementsByPage: 4, //LOS ELEMENTOS POR PAGINA DEL RANKING
        dataPage: [],
        currentPage: 1
      };
    },
    mounted() {
      fetch('/get_user')
        .then(response => {
          return response.json();
        })
        .then(data => {
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
      getPosition(index) {
        return ((this.currentPage - 1) * this.elementsByPage) + index + 1;
      },
      getDataPage(numPage){
        this.currentPage= numPage
        this.dataPage= []
        let ini= (numPage * this.elementsByPage) - this.elementsByPage
        let end= (numPage * this.elementsByPage)
        this.dataPage= this.arrayUsers.slice(ini,end)
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
  }

</script>