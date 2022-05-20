
    var image = document.getElementById("image");

    // La fonction previewPicture
    var previewPicture  = function (e) {
        // e.files contient un objet FileList
        const [picture] = e.files

        // "picture" est un objet File
        if (picture) {
            // On change l'URL de l'image
            image.src = URL.createObjectURL(picture)
        }
    }

    function red(link)
    {
        var val = document.getElementsByName('cin')[0].value;
        if(val != "")
        {
            var data = link+"?personnel="+val;
             window.open(data,link,'width=620,height=900');
        }
        else
        {
            alert("il faut ajouter d'abord le personnel")
        }
    }

window.onload = function ()
{
  //cardheader1
    const donneperso = document.getElementById('donneperso')
    donneperso.onmouseover = function (){
        donneperso.setAttribute("style","background-color: #eb3121;")
    }
    donneperso.onmouseout= function (){
        donneperso.setAttribute("style","background-color: #D42D1E;")
    }
    donneperso.onclick= function (){
        $('#persocard').fadeToggle()
        donneperso.setAttribute("class","card-header d-flex h-75")
    }

    //cardheader1
    const donneprof = document.getElementById('donneprof')
    donneprof.onmouseover = function (){
        donneprof.setAttribute("style","background-color: #eb3121;")
    }
    donneprof.onmouseout= function (){
        donneprof.setAttribute("style","background-color: #D42D1E;")
    }
    donneprof.onclick= function (){
        $('#procard').fadeToggle()
        donneprof.setAttribute("class","card-header d-flex h-75")
    }

    //imageload
    $("input[type='image']").click(function() {
        $("input[id='photo']").click();
    });

    //ajaxstatutgrade
    const sel= document.getElementById('statutgrade');
    sel.onchange= function ()
    {
        $("#grade option").remove();
        $('#op1').remove()
        $.ajax(
        {
            type:"POST",
            url: url1,
            data:{statutgrade: sel.value},
            success: function(data)
            {
                $("#grade").append(`<option  id="op2" selected></option>`);
                for(var i = 0; i < data.grades.length; i++)
                {
                    $("#grade").append(`<option value="${data.grades[i].idgrade}">${data.grades[i].gradefr}</option>`);

                }
            }
        });
    }

    //ajaxechellon
    const selgrade = document.getElementById('grade');
    var  selechellon = document.getElementById('echellon');
    var selindice = document.getElementById('indice');

    selgrade.onchange = function ()
    {
        $("#echellon option").remove();
        $("#indice option").remove();
        $('#op2').remove()
        $.ajax(
        {
            type:"POST",
            url: url2,
            data:{statutgrade: sel.value , grade:selgrade.value},
            success: function(data)
            {
                for(var i = 0; i < data.echellon.length; i++)
                {
                    $("#echellon").append(`<option>${data.echellon[i]}</option>`);
                    $("#indice").append(`<option>${data.indice[i]}</option>`);
                }

                selindice.selectedIndex = 0;
                document.getElementById('dpindice').value = selindice.options[0].text

            }
        });
    }
     function loadindice()
    {
        selindice.selectedIndex = selechellon.selectedIndex;
        document.getElementById('dpindice').value = selindice.options[selindice.selectedIndex].text
    }
    selechellon.addEventListener('change', loadindice);
}