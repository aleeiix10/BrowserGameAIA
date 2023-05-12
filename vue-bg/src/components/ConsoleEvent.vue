<template>
    
</template>
  
  <script>
  import axios from 'axios';

    export default {
    data() {
        return {
        randomNumbers: [],
        };
    },
    mounted() {
        // Realizar la solicitud GET al endpoint correspondiente
        axios.get('/ruta/django/numeros-generados/')
        .then(response => {
            // Actualizar la propiedad randomNumbers con los números obtenidos
            this.randomNumbers = response.data;
        })
        .catch(error => {
            console.error(error);
        });
    },
    };

  </script>
  