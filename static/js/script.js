function getStats() {
    $.getJSON("/api/get_users",async function(usuari){
        $('#profileStatsLevel').text(usuari.UsersObj[0].level);
        $('#profileStatsLife').text(usuari.UsersObj[0].current_life);
        $('#profileStatsMana').text(usuari.UsersObj[0].current_mana);
        $('#profileStatsExperience').text(usuari.UsersObj[0].experience);


        //Barres %
        var percentatgeVida = ((usuari.UsersObj[0].current_life)*100) / ((usuari.UsersObj[0].level*10));
        $('#profileStatsLifeBar').css({
            'background-color': 'green',
            'border-radius':'10px 0 20px 0',
            'height': '15px',
            'width': percentatgeVida + '%', //
          });
        var percentatgeMana = ((usuari.UsersObj[0].current_mana)*100) / ((usuari.UsersObj[0].level*10));
        $('#profileStatsManaBar').css({
            'background-color': 'blue',
            'border-radius':'10px 0 20px 0',
            'height': '15px',
            'width': percentatgeMana + '%', //
          });
        var percentatgeExperiencia = ((usuari.UsersObj[0].experience)*100) / ((usuari.UsersObj[0].level*10));
        $('#profileStatsExperienceBar').css({
            'background-color': 'yellow',
            'border-radius':'10px 0 20px 0',
            'height': '15px',
            'width': percentatgeExperiencia + '%', //
          });
    });
}

function getRelatedActions() {
    $.getJSON("/api/get_related_actions",async function(actions){
        $('#tbodyRelatedActions').empty();
        actions.ActionsObj.forEach(action =>{

        $('#tbodyRelatedActions').append('<tr class="border-b border-black text-center">');
        if (action.user__username == null){
            $('#tbodyRelatedActions').append(`<td class="p-2">     </td>`);
        }else{
            $('#tbodyRelatedActions').append(`<td class="p-2">`+action.user__username+`</td>`);
        }
        if (action.user_attacked__username == null){
            $('#tbodyRelatedActions').append(`<td class="p-2">     </td>`);
        }else{
            $('#tbodyRelatedActions').append(`<td class="p-2">`+action.user_attacked__username+`</td>`);
        }
        $('#tbodyRelatedActions').append(`<td class="p-2">`+action.action__name+`</td>`);
        if (action.action__category =='A'){
            $('#tbodyRelatedActions').append(`<td class="p-2">Agressiva</td>`);
        }else if (action.action__category == 'D'){
            $('#tbodyRelatedActions').append(`<td class="p-2">Defensiva</td>`);
        }else{
            $('#tbodyRelatedActions').append(`<td class="p-2">Neutral</td>`);
        }

        var timestamp = new Date(action.timestamp);
    var formattedTimestamp = timestamp.toLocaleString(); // Formato localizado de fecha y hora

        $('#tbodyRelatedActions').append(`<td class="p-2">`+formattedTimestamp+`</td>`);
        $('#tbodyRelatedActions').append(`<td class="p-2">`+action.action__cost+`</td>`);

        if (action.success == false){
            $('#tbodyRelatedActions').append(` <td class="p-2"><i class="fa fa-sharp fa-solid fa-circle-xmark" style="color: #a73131;"></i></td>`);
        }else{
            $('#tbodyRelatedActions').append(`<td class="p-2"><i class="fa fa-solid fa-circle-check" style="color: #316e32;"></i></td>`);
        }
        $('#tbodyRelatedActions').append(`</tr>`);
        })
    });
}

setTimeout(getRelatedActions, 30);
setTimeout(getStats,30); 