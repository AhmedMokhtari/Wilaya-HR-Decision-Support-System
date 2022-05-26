
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
    //data
    $(".divisiondiv").show();
     $(".districtdiv").hide();
     $(".pashalikdiv").hide();
     $(".districtpashalikdiv").hide();
     $(".annexediv").hide();
     $(".servicediv").hide();
      $(".cerclediv").hide();
      $(".caidadiv").hide();

     $("#districtpashalik").prop('required',false);
     $("#pashalik").prop('required',false);
     $("#district").prop('required',false);
     $("#annexe").prop('required',false);
     $("#dateannexe").prop('required',false);
     $("#division").prop('required',true);
     $("#service").prop('required',true);
     $("#dateservice").prop('required',true);

  //cardheader1
    const donneperso = document.getElementById('donneperso')
    if(donneperso != null)
    {
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

    }



    //imageload
    $("input[type='image']").click(function() {
        $("input[id='photo']").click();
    });

     //entite
    const selentite= document.getElementById('entite');
    selentite.onchange= function ()
    {
        if(selentite.value == "Secrétariat général")
        {
             $(".divisiondiv").show();
             $(".districtpashalikdiv").hide();
             $(".districtdiv").hide();
             $(".pashalikdiv").hide();
             $(".annexediv").hide();
             $(".cerclediv").hide();
             $(".caidadiv").hide();

             $("#districtpashalik").prop('required',false);
             $("#pashalik").prop('required',false);
             $("#district").prop('required',false);
             $("#annexe").prop('required',false);
             $("#dateannexe").prop('required',false);
             $("#division").prop('required',true);
             $("#service").prop('required',true);
             $("#dateservice").prop('required',true);
        }
        else
        {
            if(selentite.value == "Commandement")
            {
                $(".districtpashalikdiv").show();
                $(".divisiondiv").hide();
                $(".pashalikdiv").hide();
                $(".districtdiv").show();
                $(".annexediv").hide();
                $(".servicediv").hide();

                $("#districtpashalik").prop('required',true);
                $("#pashalik").prop('required',false);
                 $("#district").prop('required',true);
                 $("#annexe").prop('required',true);
                 $("#dateannexe").prop('required',true);
                 $("#division").prop('required',false);
                 $("#service").prop('required',false);
                 $("#dateservice").prop('required',false);
                 $(".cerclediv").prop('required',false);
                 $(".caidadiv").prop('required',false);
            }
        }
        if(document.getElementById("op3") == null)
         {
             $("#division").append('<option id="op3" selected></option>');

         }
         else {
            if (document.getElementById("op0") == null) {
                $("#district").append('<option id="op0" selected></option>');
            } else {
                if (document.getElementById("op4") == null) {
                    $("#cercle").append('<option id="op4" selected></option>');
                }
            }
        }


    }

    //district
    const seldistrictpash= document.getElementById('districtpashalik');
    seldistrictpash.onchange= function()
    {
        if(seldistrictpash.value == "District")
        {
             $(".divisiondiv").hide();
             $(".districtdiv").show();
             $(".pashalikdiv").hide();
             $(".servicediv").hide();
             $(".cerclediv").hide();
             $(".caidadiv").hide();

             $("#districtpashalik").prop('required',true);
             $("#pashalik").prop('required',false);
             $("#district").prop('required',true);
             $("#annexe").prop('required',true);
             $("#dateannexe").prop('required',true);
             $("#division").prop('required',false);
             $("#service").prop('required',false);
             $("#dateservice").prop('required',false);
             $("#cercle").prop('required',false);
             $("#caida").prop('required',false);
             if (document.getElementById("op4") == null)
             {
                 $("#cercle").append('<option id="op4" selected></option>');
             }

        }
        else{

            if(seldistrictpash.value == "Pashalik")
            {
                 $(".divisiondiv").hide();
                 $(".districtdiv").hide();
                 $(".pashalikdiv").show();
                 $(".annexediv").hide();
                 $(".servicediv").hide();
                 $(".cerclediv").hide();
                 $(".caidadiv").hide();

                 $("#districtpashalik").prop('required',true);
                 $("#pashalik").prop('required',true);
                 $("#district").prop('required',false);
                 $("#annexe").prop('required',false);
                 $("#dateannexe").prop('required',false);
                 $("#division").prop('required',false);
                 $("#service").prop('required',false);
                 $("#dateservice").prop('required',false);
                 $("#cercle").prop('required',false);
                  $("#caida").prop('required',false);

                 if(document.getElementById("op0") == null)
                 {
                     $("#district").append('<option id="op0" selected></option>')
                 }
                 else {
                     if (document.getElementById("op4") == null)
                     {
                        $("#cercle").append('<option id="op4" selected></option>');
                    }
                 }


            }
            else
            {
                if(seldistrictpash.value == "Cercle")
                {
                    $(".divisiondiv").hide();
                     $(".districtdiv").hide();
                     $(".pashalikdiv").hide();
                     $(".annexediv").hide();
                     $(".servicediv").hide();
                     $(".cerclediv").show();
                     $(".caidadiv").hide();

                    $("#districtpashalik").prop('required',true);
                     $("#pashalik").prop('required',false);
                     $("#district").prop('required',false);
                     $("#annexe").prop('required',false);
                     $("#dateannexe").prop('required',false);
                     $("#division").prop('required',false);
                     $("#service").prop('required',false);
                     $("#dateservice").prop('required',false);
                     $("#cercle").prop('required',true);
                     $("#caida").prop('required',true);

                     if(document.getElementById("op0") == null)
                     {
                         $("#district").append('<option id="op0" selected></option>')
                     }
                }
            }
        }
    }

    const seldistrict= document.getElementById('district');
    seldistrict.onchange= function()
    {
        $(".annexediv").show();
        $("#annexe option").remove();
        $('#op0').remove()
        $.ajax(
        {
            type:"POST",
            url: url0,
            data:{ district: seldistrict.value},
            success: function(data)
            {
                for(var i = 0; i < data.annexes.length; i++)
                {
                    $("#annexe").append(`<option value="${data.annexes[i].idannexe}">${data.annexes[i].libelleannexefr}</option>`);

                }
            }
        });
    }

    const selcercle= document.getElementById('cercle');
    selcercle.onchange= function()
    {
        $(".caidadiv").show();
        $("#caida option").remove();
        $('#op4').remove()
        $.ajax(
        {
            type:"POST",
            url: url4,
            data:{ cercle: selcercle.value},
            success: function(data)
            {
                for(var i = 0; i < data.caidas.length; i++)
                {
                    $("#caida").append(`<option value="${data.caidas[i].idcaidat}">${data.caidas[i].libellecaidatfr}</option>`);

                }
            }
        });
    }

    const seldivision= document.getElementById('division');
    seldivision.onchange= function()
    {
        $(".servicediv").show();
        $("#service option").remove();
        $('#op3').remove()
        $.ajax(
        {
            type:"POST",
            url: url3,
            data:{ division: seldivision.value},
            success: function(data)
            {
                for(var i = 0; i < data.services.length; i++)
                {
                    $("#service").append(`<option value="${data.services[i].idservice}">${data.services[i].libelleservicefr}</option>`);

                }
            }
        });
    }

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