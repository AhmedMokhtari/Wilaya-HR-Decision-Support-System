
$(document).ready(function (){
    const donneperso = document.getElementById('donneperso');
    $('#persocard').hide();
    donneperso.setAttribute("class","card-header d-flex h-75")
    //cardheader1
    if(donneperso!=null)
    {
        donneperso.onmouseover = function (){
            donneperso.setAttribute("style","background-color: #53c7cf;")
        }
        donneperso.onmouseout= function (){
            donneperso.setAttribute("style","background-color: #47BAC1;")
        }
        donneperso.onclick= function (){
            $('#persocard').fadeToggle()
            donneperso.setAttribute("class","card-header d-flex h-75")
        }
    }


    //cardheader1
    const donneprof = document.getElementById('donneprof');
    if(donneprof!=null) {
        donneprof.onmouseover = function () {
            donneprof.setAttribute("style", "background-color: #53c7cf;")
        }
        donneprof.onmouseout = function () {
            donneprof.setAttribute("style", "background-color: #47BAC1;")
        }
        donneprof.onclick = function () {
            $('#procard').fadeToggle()
            donneprof.setAttribute("class", "card-header d-flex h-75")
        }
    }
})
