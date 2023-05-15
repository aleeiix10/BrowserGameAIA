function getStats() {
    $.getJSON("/api/get_users",function(usuari){
        if($('#profileStatsLevel').text() == "" && $('#profileStatsLife').text() == "" && $('#profileStatsMana').text() == "" && $('#profileStatsExperience').text() == ""){
            $('#profileStatsLevel').text(usuari.UsersObj[0].level)
            $('#profileStatsLife').text(usuari.UsersObj[0].current_life);
            $('#profileStatsMana').text(usuari.UsersObj[0].current_mana);
            $('#profileStatsExperience').text(usuari.UsersObj[0].experience);
        }else{
            //NIVEL
            if ($('#profileStatsLevel').text() == usuari.UsersObj[0].level){
                $('#profileStatsLevel').text(usuari.UsersObj[0].level)
            }else{
                $('#profileStatsLevel').text(usuari.UsersObj[0].level).css('font-weight', 'normal').addClass('highlight');
                setTimeout(function() {
                    $('#profileStatsLevel').removeClass('highlight').css('font-weight', 'normal');
                    }, 3500);
            }
            //VIDA
            if ($('#profileStatsLife').text() == usuari.UsersObj[0].current_life){
                $('#profileStatsLife').text(usuari.UsersObj[0].current_life)
            }else{
                $('#profileStatsLife').text(usuari.UsersObj[0].current_life).css('font-weight', 'normal').addClass('highlight');
                setTimeout(function() {
                    $('#profileStatsLife').removeClass('highlight').css('font-weight', 'normal');
                    }, 3500);
            }
            //MANA
            if ($('#profileStatsMana').text() ==  usuari.UsersObj[0].current_mana){
                $('#profileStatsMana').text(usuari.UsersObj[0].current_mana)
            }else{
                $('#profileStatsMana').text(usuari.UsersObj[0].current_mana).css('font-weight', 'normal').addClass('highlight');
                setTimeout(function() {
                    $('#profileStatsMana').removeClass('highlight').css('font-weight', 'normal');
                    }, 3500);
            }
            //EXPERIENCIA
            if ($('#profileStatsExperience').text() == usuari.UsersObj[0].experience){
                $('#profileStatsExperience').text(usuari.UsersObj[0].experience)
            }else{
                $('#profileStatsExperience').text(usuari.UsersObj[0].experience).css('font-weight', 'normal').addClass('highlight');
                setTimeout(function() {
                    $('#profileStatsExperience').removeClass('highlight').css('font-weight', 'normal');
                    }, 3500);
            }
        }

        //Barres %
        var percentatgeVida = ((usuari.UsersObj[0].current_life)*100) / ((usuari.UsersObj[0].level*10));
        $('#profileStatsLifeBar').css({
            'background-color': 'green',
            'border-radius': '10px 0 20px 0',
            'height': '15px',
            'width': '0%', // especifica un valor inicial para el ancho
            'transition': 'width 1s ease-out', // especifica una duración y función de transición para la propiedad 'width'
        }).width(percentatgeVida + '%'); 
        var percentatgeMana = ((usuari.UsersObj[0].current_mana)*100) / ((usuari.UsersObj[0].level*10));
        $('#profileStatsManaBar').css({
            'background-color': 'blue',
            'border-radius': '10px 0 20px 0',
            'height': '15px',
            'width': '0%', // especifica un valor inicial para el ancho
            'transition': 'width 1s ease-out', // especifica una duración y función de transición para la propiedad 'width'
        }).width(percentatgeMana + '%'); 
        var percentatgeExperiencia = ((usuari.UsersObj[0].experience)*100) / ((usuari.UsersObj[0].level*10));
        $('#profileStatsExperienceBar').css({
            'background-color': 'yellow',
            'border-radius': '10px 0 20px 0',
            'height': '15px',
            'width': '0%', // especifica un valor inicial para el ancho
            'transition': 'width 1s ease-out', // especifica una duración y función de transición para la propiedad 'width'
        }).width(percentatgeExperiencia + '%'); 
    });
}

function getRelatedActions() {
    $.getJSON("/api/get_related_actions",function(actions){
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
function getActions() {
    $.getJSON("/api/get_actions",function(actions){
        actions.ActionsObj.forEach(action =>{
            $('#tbodyAtacs').append('<tr class="border-b border-black text-center">');
            $('#tbodyAtacs').append(`<td class="p-2">`+action.name+`</td>`);
            if (action.category =='A'){
               $('#tbodyAtacs').append(`<td class="p-2">Agressiva</td>`);
            }else if (action.category  == 'D'){
               $('#tbodyAtacs').append(`<td class="p-2">Defensiva</td>`);
            }else{
               $('#tbodyAtacs').append(`<td class="p-2">Neutral</td>`);
            }
            
            $('#tbodyAtacs').append(`<td class="p-2 text-center">`+action.cost+`</td>`);
            $('#tbodyAtacs').append(`<td class="p-2 text-center">`+action.succesPercentage+`</td>`);
            $('#tbodyAtacs').append(`<td class="p-2 text-center">`+action.points+`</td>`);
            $('#tbodyAtacs').append('</tr>');
        })
    });
}
function getPopUps() {
   $(".botonAccion").hover(function(){
        var popoverId = $(this).data('popover');
        $("#" + popoverId).toggleClass('invisible');
        $("#" + popoverId).toggleClass('opacity-100');
    });  
}
  

  


function getUserRanking(username) {
    $.getJSON("/api/get_userByUsername/"+username,function(usuari){
        $('#profileNom').text(usuari.userObj[0].username);
        $('#profileNivell').text(usuari.userObj[0].level);
        var accionsExitoses = 0;
        var accionsFallides = 0;
        var totalAccions = 0;
        if (usuari.actionObj.length == 0){
            $('#noActions').text("Aquest ususari no te atacs realitzats");
        }else{
            usuari.actionObj.forEach(atac => {
            totalAccions +=1;
            if (atac.success == true) {
                accionsExitoses +=1;
            }else if (atac.success == false) {
                accionsFallides +=1;
            }
        });
        var percentatgeExitoses = (accionsExitoses/totalAccions)*100;
        var percentatgeFallides = (accionsFallides/totalAccions)*100;
        var ctx = document.getElementById('myChart').getContext('2d');
        var myChart = new Chart(ctx, {
            type: 'pie',
            data: {

                labels: ['Atacs Exitosos', 'Atacs Fallits'],
                datasets: [{
                    label: "Percentatge",
                    data: [percentatgeExitoses, percentatgeFallides],
                    backgroundColor: ['#15803d', '#14532d']
                }]
            },
            options: {
                responsive: false,
                maintainAspectRatio: false,
                width: 400,
                height: 400
            }
        });
    }  
    });
    $.getJSON("/get_user", function(user) {
        const index = user.users.findIndex((user) => user.username === username);
        if (index !== -1) {
            const position = index + 1;
            $('#profilprofileNomPosicio').text(position);
        }
    });
    
}

function fertilitzant(acciones){
    const rutaImagen = "";
    const rutaImagenVerdura = "/static/img/verdura1.png";
    for (let i = 0; i < acciones.length; i++) {
        if(i==8) {
            acciones[i].style.backgroundImage = `url(${rutaImagenVerdura})`;
            acciones[i].id = "verdura"+(i+1);
            acciones[i].classList.add("animacion-verdura-exp");
        }
        else {
            acciones[i].style.backgroundImage = `url(${rutaImagen})`;
            acciones[i].id = (i+1);
        }
    }
    acciones.forEach(pea => {
        pea.classList.remove("animacion-pea");
        pea.classList.remove("animacion-carrot");
        pea.classList.remove("animacion-beet");
        pea.classList.remove("animacion-estate");
        pea.classList.remove("animacion-verdura");
        pea.classList.remove("animacion-cura");
        pea.classList.remove("animacion-sun");
        pea.classList.remove("animacion-verdura-rafaga");
        pea.classList.remove("animacion-verdura-rayo");
        pea.classList.remove("animacion-verdura-guisantes");
        pea.classList.remove("animacion-verdura-mancha");
        pea.classList.remove("animacion-verdura-zanahoria");
        pea.classList.remove("animacion-verdura-exp");
        pea.classList.remove("animacion-verdura-nivel");
        pea.classList.remove("animacion-exp");
        pea.classList.remove("animacion-verdura-muerte");
        pea.classList.remove("animacion-calavera");
        pea.classList.remove("animacion-onion");
        void pea.offsetWidth; // Reiniciar la animación
        if(pea.id == "verdura9") {
            pea.classList.add("animacion-verdura-exp");
        }
    });
}

function sol(acciones){
    const rutaImagen = "/static/img/sol.png";
    const rutaImagenVerdura = "/static/img/verdura1sol.png";
    const rutaImagenCura = "/static/img/verdura2.png";
    for (let i = 0; i < acciones.length; i++) {
        if(i==0) {
            acciones[i].style.backgroundImage = `url(${rutaImagenVerdura})`;
            acciones[i].id = "verdura"+(i+1);
            acciones[i].classList.add("animacion-verdura");
        }
        else if(i==1) {
            acciones[i].style.backgroundImage = `url(${rutaImagen})`;
            acciones[i].id = "sun"+(i+1);
            acciones[i].classList.add("animacion-sun");
        }
        else {
            acciones[i].style.backgroundImage = `url(${rutaImagenCura})`;
            acciones[i].id = "cura"+(i+1);
            acciones[i].classList.add("animacion-cura");
        }
    }
    acciones.forEach(pea => {
        pea.classList.remove("animacion-pea");
        pea.classList.remove("animacion-carrot");
        pea.classList.remove("animacion-onion");
        pea.classList.remove("animacion-beet");
        pea.classList.remove("animacion-verdura");
        pea.classList.remove("animacion-cura");
        pea.classList.remove("animacion-estate");
        pea.classList.remove("animacion-verdura-rafaga");
        pea.classList.remove("animacion-verdura-rayo");
        pea.classList.remove("animacion-verdura-guisantes");
        pea.classList.remove("animacion-verdura-mancha");
        pea.classList.remove("animacion-verdura-zanahoria");
        pea.classList.remove("animacion-verdura-exp");
        pea.classList.remove("animacion-verdura-nivel");
        pea.classList.remove("animacion-exp");
        pea.classList.remove("animacion-verdura-muerte");
        pea.classList.remove("animacion-calavera");
        pea.classList.remove("animacion-sun");
        void pea.offsetWidth; // Reiniciar la animación
        if(pea.id == "verdura1") {
            pea.classList.add("animacion-verdura");
        }
        else if(pea.id == "sun2") {
            pea.classList.add("animacion-sun");
        }
        else{
            pea.classList.add("animacion-cura");
        }
    });
}

function arrels(acciones){
    const rutaImagen = "/static/img/raices.png";
    const rutaImagenVerdura = "/static/img/verdura1.png";
    const rutaImagenCura = "/static/img/verdura2.png";
    for (let i = 0; i < acciones.length; i++) {
        if(i==0) {
            acciones[i].style.backgroundImage = `url(${rutaImagenVerdura})`;
            acciones[i].id = "verdura"+(i+1);
            acciones[i].classList.add("animacion-verdura");
        }
        else if(i==1) {
            acciones[i].style.backgroundImage = `url(${rutaImagen})`;
            acciones[i].id = "estate"+(i+1);
            acciones[i].classList.add("animacion-estate");
        }
        else {
            acciones[i].style.backgroundImage = `url(${rutaImagenCura})`;
            acciones[i].id = "cura"+(i+1);
            acciones[i].classList.add("animacion-cura");
        }
    }
    acciones.forEach(pea => {
        pea.classList.remove("animacion-pea");
        pea.classList.remove("animacion-carrot");
        pea.classList.remove("animacion-onion");
        pea.classList.remove("animacion-beet");
        pea.classList.remove("animacion-verdura");
        pea.classList.remove("animacion-cura");
        pea.classList.remove("animacion-sun");
        pea.classList.remove("animacion-verdura-rafaga");
        pea.classList.remove("animacion-verdura-rayo");
        pea.classList.remove("animacion-verdura-guisantes");
        pea.classList.remove("animacion-verdura-mancha");
        pea.classList.remove("animacion-verdura-zanahoria");
        pea.classList.remove("animacion-verdura-exp");
        pea.classList.remove("animacion-verdura-nivel");
        pea.classList.remove("animacion-exp");
        pea.classList.remove("animacion-verdura-muerte");
        pea.classList.remove("animacion-calavera");
        pea.classList.remove("animacion-estate");
        void pea.offsetWidth; // Reiniciar la animación
        if(pea.id == "verdura1") {
            pea.classList.add("animacion-verdura");
        }
        else if(pea.id == "estate2") {
            pea.classList.add("animacion-estate");
        }
        else{
            pea.classList.add("animacion-cura");
        }
    });
}

function remolatxa(acciones){
    const rutaImagen = "/static/img/remolacha.png";
    const rutaImagenVerdura = "/static/img/verdura1.png";
    for (let i = 0; i < acciones.length; i++) {
        if(i==8) {
            acciones[i].style.backgroundImage = `url(${rutaImagenVerdura})`;
            acciones[i].id = "verdura"+(i+1);
            acciones[i].classList.add("animacion-verdura-rayo");
        }
        else {
            acciones[i].style.backgroundImage = `url(${rutaImagen})`;
            acciones[i].id = "beet"+(i+1);
        }
    }
    acciones.forEach(pea => {
        pea.classList.remove("animacion-pea");
        pea.classList.remove("animacion-carrot");
        pea.classList.remove("animacion-onion");
        pea.classList.remove("animacion-estate");
        pea.classList.remove("animacion-verdura");
        pea.classList.remove("animacion-cura");
        pea.classList.remove("animacion-sun");
        pea.classList.remove("animacion-verdura-rafaga");
        pea.classList.remove("animacion-verdura-rayo");
        pea.classList.remove("animacion-verdura-guisantes");
        pea.classList.remove("animacion-verdura-mancha");
        pea.classList.remove("animacion-verdura-zanahoria");
        pea.classList.remove("animacion-verdura-exp");
        pea.classList.remove("animacion-verdura-nivel");
        pea.classList.remove("animacion-exp");
        pea.classList.remove("animacion-verdura-muerte");
        pea.classList.remove("animacion-calavera");
        pea.classList.remove("animacion-beet");
        void pea.offsetWidth; // Reiniciar la animación
        if(pea.id == "verdura9") {
            pea.classList.add("animacion-verdura-rayo");
        }
        else {
            pea.classList.add("animacion-beet");
        }
    });
}

function ceba(acciones){
    const rutaImagen = "/static/img/cebolla.png";
    const rutaImagenVerdura = "/static/img/verdura1.png";
    for (let i = 0; i < acciones.length; i++) {
        if(i==8) {
            acciones[i].style.backgroundImage = `url(${rutaImagenVerdura})`;
            acciones[i].id = "verdura"+(i+1);
            acciones[i].classList.add("animacion-verdura-rafaga");
        }
        else {
            acciones[i].style.backgroundImage = `url(${rutaImagen})`;
            acciones[i].id = "onion"+(i+1);
        }
    }
    acciones.forEach(pea => {
        pea.classList.remove("animacion-pea");
        pea.classList.remove("animacion-carrot");
        pea.classList.remove("animacion-beet");
        pea.classList.remove("animacion-estate");
        pea.classList.remove("animacion-verdura");
        pea.classList.remove("animacion-cura");
        pea.classList.remove("animacion-sun");
        pea.classList.remove("animacion-verdura-rafaga");
        pea.classList.remove("animacion-verdura-rayo");
        pea.classList.remove("animacion-verdura-guisantes");
        pea.classList.remove("animacion-verdura-mancha");
        pea.classList.remove("animacion-verdura-zanahoria");
        pea.classList.remove("animacion-verdura-exp");
        pea.classList.remove("animacion-verdura-nivel");
        pea.classList.remove("animacion-exp");
        pea.classList.remove("animacion-verdura-muerte");
        pea.classList.remove("animacion-calavera");
        pea.classList.remove("animacion-onion");
        void pea.offsetWidth; // Reiniciar la animación
        if(pea.id == "verdura9") {
            pea.classList.add("animacion-verdura-rafaga");
        }
        else {
            pea.classList.add("animacion-onion");
        }
        
    });
}

function pastanaga(acciones){
    const rutaImagen = "/static/img/zanahoria.png";
    const rutaImagenVerdura = "/static/img/verdura1.png";
    for (let i = 0; i < acciones.length; i++) {
        if(i==8) {
            acciones[i].style.backgroundImage = `url(${rutaImagenVerdura})`;
            acciones[i].id = "verdura"+(i+1);
            acciones[i].classList.add("animacion-verdura-zanahoria");
        }
        else {
            acciones[i].style.backgroundImage = `url(${rutaImagen})`;
            acciones[i].id = "carrot"+(i+1);
        }   
    }
    acciones.forEach(pea => {
        pea.classList.remove("animacion-pea");
        pea.classList.remove("animacion-onion");
        pea.classList.remove("animacion-beet");
        pea.classList.remove("animacion-estate");
        pea.classList.remove("animacion-verdura");
        pea.classList.remove("animacion-cura");
        pea.classList.remove("animacion-sun");
        pea.classList.remove("animacion-verdura-rafaga");
        pea.classList.remove("animacion-verdura-rayo");
        pea.classList.remove("animacion-verdura-guisantes");
        pea.classList.remove("animacion-verdura-mancha");
        pea.classList.remove("animacion-verdura-zanahoria");
        pea.classList.remove("animacion-verdura-exp");
        pea.classList.remove("animacion-verdura-nivel");
        pea.classList.remove("animacion-exp");
        pea.classList.remove("animacion-verdura-muerte");
        pea.classList.remove("animacion-calavera");
        pea.classList.remove("animacion-carrot");
        void pea.offsetWidth; // Reiniciar la animación
        if(pea.id == "verdura9") {
            pea.classList.add("animacion-verdura-zanahoria");
        }
        else {
            pea.classList.add("animacion-carrot");
        }
    });
}

function pesols(acciones){
    const rutaImagen = "/static/img/guisante.png";
    const rutaImagenVerdura = "/static/img/verdura1.png";
    const rutaImagenMancha = "/static/img/mancha.png";
    for (let i = 0; i < acciones.length; i++) {
        if(i==8) {
            acciones[i].style.backgroundImage = `url(${rutaImagenVerdura})`;
            acciones[i].id = "verdura"+(i+1);
            acciones[i].classList.add("animacion-verdura-guisantes");
        }
        else if(i==7){
            acciones[i].style.backgroundImage = `url(${rutaImagenMancha})`;
            acciones[i].id = "mancha"+(i+1);
            acciones[i].classList.add("animacion-verdura-mancha");
        }
        else {
            acciones[i].style.backgroundImage = `url(${rutaImagen})`;
            acciones[i].id = "pea"+(i+1);
        }
    }

    acciones.forEach(pea => {
        pea.classList.remove("animacion-carrot");
        pea.classList.remove("animacion-onion");
        pea.classList.remove("animacion-beet");
        pea.classList.remove("animacion-estate");
        pea.classList.remove("animacion-verdura");
        pea.classList.remove("animacion-cura");
        pea.classList.remove("animacion-sun");
        pea.classList.remove("animacion-verdura-rafaga");
        pea.classList.remove("animacion-verdura-rayo");
        pea.classList.remove("animacion-verdura-guisantes");
        pea.classList.remove("animacion-verdura-mancha");
        pea.classList.remove("animacion-verdura-zanahoria");
        pea.classList.remove("animacion-verdura-exp");
        pea.classList.remove("animacion-verdura-nivel");
        pea.classList.remove("animacion-exp");
        pea.classList.remove("animacion-verdura-muerte");
        pea.classList.remove("animacion-calavera");
        pea.classList.remove("animacion-pea");
        void pea.offsetWidth; // Reiniciar la animación
        if(pea.id == "verdura9") {
            pea.classList.add("animacion-verdura-guisantes");
        }
        else if(pea.id == "mancha8") {
            pea.classList.add("animacion-verdura-mancha");
        }
        else {
            pea.classList.add("animacion-pea");
        }
    });
}

function levelUp(acciones){
    $(".contenedorAcciones").css("z-index", "9999");
    setTimeout(function() {
        $(".contenedorAcciones").removeAttr("style");
    }, 3000);
    const rutaImagen = "/static/img/exp.png";
    const rutaImagenVerdura = "/static/img/verdura1.png";
    for (let i = 0; i < acciones.length; i++) {
        if(i==8) {
            acciones[i].style.backgroundImage = `url(${rutaImagenVerdura})`;
            acciones[i].id = "verdura"+(i+1);
            acciones[i].classList.add("animacion-verdura-nivel");
        }
        else {
            acciones[i].style.backgroundImage = `url(${rutaImagen})`;
            acciones[i].id = "exp"+(i+1);
        }
    }
    acciones.forEach(pea => {
        pea.classList.remove("animacion-pea");
        pea.classList.remove("animacion-carrot");
        pea.classList.remove("animacion-onion");
        pea.classList.remove("animacion-estate");
        pea.classList.remove("animacion-verdura");
        pea.classList.remove("animacion-cura");
        pea.classList.remove("animacion-sun");
        pea.classList.remove("animacion-verdura-rafaga");
        pea.classList.remove("animacion-verdura-rayo");
        pea.classList.remove("animacion-verdura-guisantes");
        pea.classList.remove("animacion-verdura-mancha");
        pea.classList.remove("animacion-verdura-zanahoria");
        pea.classList.remove("animacion-verdura-exp");
        pea.classList.remove("animacion-verdura-nivel");
        pea.classList.remove("animacion-exp");
        pea.classList.remove("animacion-verdura-muerte");
        pea.classList.remove("animacion-calavera");
        pea.classList.remove("animacion-beet");
        void pea.offsetWidth; // Reiniciar la animación
        if(pea.id == "verdura9") {
            pea.classList.add("animacion-verdura-nivel");
        }
        else {
            pea.classList.add("animacion-exp");
        }
    });
}

