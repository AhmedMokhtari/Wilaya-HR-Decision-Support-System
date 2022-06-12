
$(document).ready(function (){
    const donneperso = document.getElementById('donneperso');
    $('#persocard').hide();
    donneperso.setAttribute("class","card-header d-flex h-75")

    if(donneperso!=null)
    {
        donneperso.onclick= function (){
            $('#persocard').fadeToggle()
            donneperso.setAttribute("class","card-header d-flex h-75")
        }
    }


    //cardheader1
    const donneprof = document.getElementById('donneprof');
    if(donneprof!=null) {
        donneprof.onclick = function () {
            $('#procard').fadeToggle()
            donneprof.setAttribute("class", "card-header d-flex h-75")
        }
    }
})
