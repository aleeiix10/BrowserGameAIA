<template>
    <ul>
        <li v-for="(info, index) in arrayInfo" :key="index">- {{info.name}}: {{ info.random }}/{{ info.prob }} {{info.time}} {{ info.success }}</li>
    </ul>
</template>
  
<script>

export default {
    el: '#modalVue',
    name: "ConsoleEvent",
    data() {
        return {
        arrayInfo: [],
        };
    },
    mounted() {
        fetch('/save_action')
            .then(response => {
            return response.json();
            })
            .then(data => {
                let arrayTime= this.changeFormatTime(data.arrayTime)
                let arrayArrayActions= this.turntoArray(data.arrayAction)
                let arrayNameActions= this.turnToArray(arrayArrayActions, 0)
                let arrayPorcentageActions= this.turnToArray(arrayArrayActions, 1)
                this.arrayInfo= this.addInfoIntoArray(arrayNameActions, arrayPorcentageActions, data.arrayRandom, data.arraySuccess, arrayTime)
            })
            .catch(error => {
            console.log(error);
            })
    },
    methods:{
        turntoArray(arrayArray){
            let arrayInfoConsole= []
            arrayArray.forEach(array => {
                array.forEach(element=>{
                    let arrayInfo= []
                    for (let key in element) {
                        if (Object.prototype.hasOwnProperty.call(element, key)) {
                            arrayInfo.push(element[key])
                        }
                    }
                    arrayInfoConsole.push(arrayInfo)
                })
            });
            return arrayInfoConsole
        },

        addInfoIntoArray(arrayName, arrayPorcentage, arrayRandom, arraySuccess, arrayTime){
            let arrayInfo= []

            for (let index = 0; index < arrayName.length; index++) {
                let dict= {}
                dict.name= arrayName[index]
                dict.prob= arrayPorcentage[index]
                dict.random= arrayRandom[index]
                dict.success= arraySuccess[index]
                dict.time= arrayTime[index]
                arrayInfo.push(dict)
            }
            return arrayInfo
        },

        turnToArray(arrayObj, index){
            let arrayReturn= []
            arrayObj.forEach(array => {
                arrayReturn.push(array[index])
            });
            return arrayReturn
        },

        changeFormatTime(arrayTime){
            let arrayFormatTime= []
            arrayTime.forEach(element => {
                var timestamp = new Date(element);
                var formattedTimestamp = timestamp.toLocaleString();
                arrayFormatTime.push(formattedTimestamp)
            });
            return (arrayFormatTime)
        }
    }
};

</script>
  