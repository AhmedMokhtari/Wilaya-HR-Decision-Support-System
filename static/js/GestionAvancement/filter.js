       document.getElementById('formsearch').addEventListener('change',function (e){
            document.getElementById('personneldata').value=''
            let val= e.target.getAttribute('name') +'&'+e.target.value  
            ajaxPerso(val)
            ajaxYearsEmpty(val)

      })

      function ajaxPerso(selected){ 
        $.ajax({
            type: 'get',
            url: `ajaxfilter/${selected}/`,
            success: function(response){
               const persoData = response.data
              dataa=JSON.parse(persoData) 
              select=document.getElementById('datalistOptions')
              select.innerHTML=""
              for (let i=0;i<dataa.length;i++){
                select.innerHTML+=`<option value="${dataa[i]}"></option>`
             }
             
            },
            error: function(error){
                console.log(error)
            }
        })
    }
    function ajaxYearsEmpty(selected){
        let table=$('#table').DataTable()
        table.clear().draw();
        $.ajax({
            type: 'get',
            url: `ajaxfilteryearmpty/${selected}/`,
            success: function(response){
                const persoData =JSON.parse(response.data)
                console.log(persoData)
                persoData.forEach(item=>{
                    let table =$('#table').DataTable();
                    let idpersonnel = item.id;
                    table.row.add([
                        item.cin,
                        item.name ,
                        item.year,
                        `<span class="btn btn-primary addyear"><i class="fa fa-plus" aria-hidden="true"></i></span>`,
                        `<a href="http://127.0.0.1:8000/personnel/personnelinfo/${idpersonnel}" class="btn btn-success m-1"><i class="fa-solid fa-arrow-up-right-from-square fa-lg " ></i></a>`
                    ]).draw();
                })
                $('.addyear').on('click', function(){
                    document.getElementById('annee').innerHTML = `<option selected>${$(this).parents('tr').find("td:eq(2)").text()}</option>`;
                    document.getElementById('personneldata').value = $(this).parents('tr').find("td:eq(0)").text();
                });
            },
            error: function(error){
                console.log(error)
            }
        })
    }
window.onload = function ()
{
    console.log('teeeeeeeeeeeeeeeee')
    document.getElementById('personneldata').setAttribute("pattern",patt)
    function frontivision(){
        $(".divisiondiv").show() 
         $(".districtpashalikdiv").hide() 
         $(".districtdiv").hide() 
         $(".pashalikdiv").hide() 
         $(".annexediv").hide() 
         $(".cerclediv").hide() 
         $(".caidadiv").hide() 
          $(".servicediv").hide() 
    }
    function front(){
        $(".divisiondiv").hide() 
         $(".districtpashalikdiv").hide() 
         $(".districtdiv").hide() 
         $(".pashalikdiv").hide() 
         $(".annexediv").hide() 
         $(".cerclediv").hide() 
         $(".caidadiv").hide() 
          $(".servicediv").hide() 
    }
    const selentite= document.getElementById('entite') 
    //data
    if(selentite != null) {
        front() 
    }
    function divisionDefault(){
        $("#division option").remove() 
        $("#division").append('<option  style="display: none"></option>') 
    }
    function serviceDefault(){
        $("#service option").remove() 
        $("#service").append('<option style="display: none"></option>') 
    }
    function cercleDefault(){
        $('#cercle').val('') 
    }
    function caidaDefault(){
        $("#caida option").remove() 
        $("#caida").append('<option style="display: none"></option>') 
    }
    function districtDefault(){
        //$("#district option").remove() 
        $('#district').val('') 
    }
    function annexeDefault(){
        $("#annexe option").remove() 
        $("#annexe").append('<option style="display: none"></option>') 
    }
    function pashalikDefault(){
        $('#pashalik').val('') 
    }
    function districtPashaslikCercleDefault(){
        $('#districtpashalik').val('') 
    }


    divisionDefault() 
    serviceDefault() 
    cercleDefault() 
    caidaDefault() 
    districtDefault() 
    annexeDefault() 
    pashalikDefault() 
    districtPashaslikCercleDefault() 
    //entite

    function ajaxdivision(){
        if(selentite != null) {
            $("#division option").remove() 
            $.ajax(
                {
                    type: "POST",
                    url: url6,
                    data: {entite: selentite.value},
                    success: function (data) {
                        $("#division").append(`<option value="" style="display: none" ></option>`) 
                        for (var i = 0 ; i < data.divisions.length ; i++) {
                            $("#division").append(`<option value="${data.divisions[i].iddivision}">${data.divisions[i].libelledivisionfr}</option>`) 
                        }
                    }
                }) 
        }
    }

    if(selentite!=null) {
        selentite.onchange = function () {
            divisionDefault() 
            serviceDefault() 
            cercleDefault() 
            caidaDefault() 
            districtDefault() 
            annexeDefault() 
            pashalikDefault() 
            districtPashaslikCercleDefault() 
            districtPashaslikCercleDefault() 
            if (selentite.value == "Secrétariat général") {
                frontivision() 
                ajaxdivision() 
            }else if(selentite.value == "Commandement"){
                    $(".districtpashalikdiv").show() 
                    $(".divisiondiv").hide() 
                    $(".pashalikdiv").hide() 
                    $(".districtdiv").hide() 
                    $(".annexediv").hide() 
                    $(".servicediv").hide() 

            }else if (selentite.value == "Dai" || selentite.value == "Cabinet" || selentite.value == "Dsic") {
                        frontivision() 
                        ajaxdivision() 
        }
    }

    //district
    const seldistrictpash= document.getElementById('districtpashalik') 
    if(seldistrictpash != null) {
        seldistrictpash.onchange = function () {
            if (seldistrictpash.value == "District") {
                $(".divisiondiv").hide() 
                $(".districtdiv").show() 
                $(".pashalikdiv").hide() 
                $(".servicediv").hide() 
                $(".cerclediv").hide() 
                $(".caidadiv").hide() 
                divisionDefault() 
                serviceDefault() 
                cercleDefault() 
                caidaDefault() 
                districtDefault() 
                annexeDefault() 
                pashalikDefault() 
            } else {

                if (seldistrictpash.value == "Pashalik") {
                    $(".divisiondiv").hide() 
                    $(".districtdiv").hide() 
                    $(".pashalikdiv").show() 
                    $(".annexediv").hide() 
                    $(".servicediv").hide() 
                    $(".cerclediv").hide() 
                    $(".caidadiv").hide() 
                    divisionDefault() 
                    serviceDefault() 
                    cercleDefault() 
                    caidaDefault() 
                    districtDefault() 
                    annexeDefault() 
                    pashalikDefault() 
                } else {
                    if (seldistrictpash.value == "Cercle") {
                        $(".divisiondiv").hide() 
                        $(".districtdiv").hide() 
                        $(".pashalikdiv").hide() 
                        $(".annexediv").hide() 
                        $(".servicediv").hide() 
                        $(".cerclediv").show() 
                        $(".caidadiv").hide() 
                        divisionDefault() 
                        serviceDefault() 
                        cercleDefault() 
                        caidaDefault() 
                        districtDefault() 
                        annexeDefault() 
                        pashalikDefault() 
                    }
                }
            }
        }
    }

    const seldistrict= document.getElementById('district') 
    seldistrict.onchange= function()
    {
        $(".annexediv").show() 
        $("#annexe option").remove() 
        divisionDefault() 
        serviceDefault() 
        cercleDefault() 
        caidaDefault() 
        annexeDefault() 
        pashalikDefault() 
        $.ajax(
        {
            type:"POST",
            url: url0,
            data:{ district: seldistrict.value},
            success: function(data)
            {
                for(var i = 0; i < data.annexes.length ; i++)
                {
                    $("#annexe").append(`<option value="${data.annexes[i].idannexe}">${data.annexes[i].libelleannexefr}</option>`) 

                }
            }
        }) 
    }

    const selcercle= document.getElementById('cercle') 
    selcercle.onchange= function()
    {
        $(".caidadiv").show() 
        $("#caida option").remove() 
        divisionDefault() 
        serviceDefault() 
        caidaDefault() 
        districtDefault() 
        annexeDefault() 
        pashalikDefault() 
        $.ajax(
        {
            type:"POST",
            url: url4,
            data:{ cercle: selcercle.value},
            success: function(data)
            {
                for(var i = 0 ;i < data.caidas.length ; i++)
                {
                    $("#caida").append(`<option value="${data.caidas[i].idcaidat}">${data.caidas[i].libellecaidatfr}</option>`) 

                }
            }
        }) 
    }

    const seldivision= document.getElementById('division') 
    seldivision.onchange= function()
    {
        $(".servicediv").show() 
        $("#service option").remove() 
        serviceDefault() 
        cercleDefault() 
        caidaDefault() 
        districtDefault() 
        annexeDefault() 
        pashalikDefault() 
        $.ajax(
        {
            type:"POST",
            url: url3,
            data:{ division: seldivision.value},
            success: function(data)
            {
                for(var i = 0 ; i < data.services.length ; i++)
                {
                    $("#service").append(`<option value="${data.services[i].idservice}">${data.services[i].libelleservicefr}</option>`) 

                }
            }
        }) 
    }

}
}