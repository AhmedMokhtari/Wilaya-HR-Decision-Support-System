       document.getElementById('formsearch').addEventListener('change',function (e){
            let entite=$("#entite");
            let division=$('#division');
            let service=$('#service');
            let districtpashalik=$('#districtpashalik');
            let district=$('#district');
            let annexe=$('#annexe');
            let pashalik=$('#pashalik');
            let cercle=$('#cercle');
            let caida=$('#caida');
          if(e.target.getAttribute('name')=='statutgrade' || e.target.getAttribute('name')=='grade' || e.target.getAttribute('name')=='radioGenre'){
              /*console.log('entite',entite.val())
              console.log('cercle',cercle.val())
              console.log('pashalik',pashalik.val())
              console.log('distric',district.val())     */
              let statutgrade=document.getElementById('statutgrade').value;
              let gradeper=document.getElementById('grade').value;
              let radioval=$('input[name=radioGenre]:checked', '#formsearch').val()

                if(entite.val()!=''){
                  if(division.val()!='') {
                      if (service.val() != '') {
                            console.log('filter service')
                            let val= service.attr("name") +'&'+service.val()+'&'+statutgrade+'&'+gradeper+'&'+radioval;
                            ajaxPerso(val)

                      }else {
                          let val= division.attr("name") +'&'+division.val()+'&'+statutgrade+'&'+gradeper+'&'+radioval;
                          ajaxPerso(val)
                      }
                  }else if(districtpashalik.val()!=''){
                            if(district.val()!=''){
                                if(annexe.val()!=''){
                                    let val= annexe.attr("name") +'&'+annexe.val()+'&'+statutgrade+'&'+gradeper+'&'+radioval;
                                     ajaxPerso(val)
                                }else{
                                    let val= district.attr("name") +'&'+district.val()+'&'+statutgrade+'&'+gradeper+'&'+radioval;
                                     ajaxPerso(val)
                                }
                            }else if(pashalik.val()!=''){
                                let val= pashalik.attr("name") +'&'+pashalik.val()+'&'+statutgrade+'&'+gradeper+'&'+radioval;
                                ajaxPerso(val)
                            }else if(cercle.val()!=''){
                                if(caida.val()!=''){
                                    let val= caida.attr("name") +'&'+caida.val()+'&'+statutgrade+'&'+gradeper+'&'+radioval;
                                     ajaxPerso(val)
                                }else{
                                    let val= cercle.attr("name") +'&'+cercle.val()+'&'+statutgrade+'&'+gradeper+'&'+radioval;
                                     ajaxPerso(val)
                                }
                            }else{
                               // console.log('filter with sdd' +districtpashalik)
                                let val= districtpashalik.attr("name") +'&'+districtpashalik.val()+'&'+statutgrade+'&'+gradeper+'&'+radioval;
                                ajaxPerso(val)
                            }
                  }else{
                            //console.log('filter with '+entite.val())
                            let val= entite.attr("name") +'&'+entite.val()+'&'+statutgrade+'&'+gradeper+'&'+radioval;
                            ajaxPerso(val)
                  }
              }else{
                let val='All&All&'+statutgrade+'&'+gradeper+'&'+radioval;
                ajaxPerso(val)
              }
          }
          else{
            let statutgrade=document.getElementById('statutgrade').value;
            let gradeper=document.getElementById('grade').value;
            let radioval=$('input[name=radioGenre]:checked', '#formsearch').val()
            let val= e.target.getAttribute('name') +'&'+e.target.value+'&'+statutgrade+'&'+gradeper+'&'+radioval;
            ajaxPerso(val)
          }
      })

 function ajaxPerso(selectedbudget){
    let table=$('#table').DataTable()
    table.clear().draw();
    $.ajax({
        type: 'get',
        url: `perso-json/${selectedbudget}/`,
        success: function(response){
            const persoData = response.data
            //let tb1 = document.querySelector('#tbody');
           // tb1.innerHTML=""
          dataa=JSON.parse(persoData);
          console.log(dataa)
          let tb1 = document.querySelector('#imglist');
           tb1.innerHTML=""
           dataa.map(item=>{
               let idp = item.idpersonnel;
              personnels=`<div class="col-lg-8 col-xs-12 col-centered">
              <div class="card-container">  
                  <div class="card-vertical">
                      <div class="card-front">
                          <img src="https://upload.wikimedia.org/wikipedia/commons/b/b9/Steve_Jobs_Headshot_2010-CROP.jpg">
                      </div>
                      
                          <div class="card-back clippath">
                              <a href="personnel/personnelinfo/${idp}"></a>
                              <article class="card-back-content ">
                                  <h1>${item.nomfr} ${item.prenomfr} </h1>
                                  <p>${item.cin}</p>
                                  <p>${item.idservice_field__libelleservicear}</p>
                              <article>
                               </a>
                          </div>
                  </div>
              </div>
      </div>`
           tb1.innerHTML+=personnels;
           })
        },
        error: function(error){
            console.log(error)
        }
    })
}

window.onload = function ()
{
    function frontivision(){
        $(".divisiondiv").show();
         $(".districtpashalikdiv").hide();
         $(".districtdiv").hide();
         $(".pashalikdiv").hide();
         $(".annexediv").hide();
         $(".cerclediv").hide();
         $(".caidadiv").hide();
          $(".servicediv").hide();
    }
    function front(){
        $(".divisiondiv").hide();
         $(".districtpashalikdiv").hide();
         $(".districtdiv").hide();
         $(".pashalikdiv").hide();
         $(".annexediv").hide();
         $(".cerclediv").hide();
         $(".caidadiv").hide();
          $(".servicediv").hide();
    }
    const selentite= document.getElementById('entite');
    //data
    if(selentite != null) {
        front();
    }
    function divisionDefault(){
        $("#division option").remove();
        $("#division").append('<option  style="display: none"></option>');
    }
    function serviceDefault(){
        $("#service option").remove();
        $("#service").append('<option style="display: none"></option>');
    }
    function cercleDefault(){
        $('#cercle').val('');
    }
    function caidaDefault(){
        $("#caida option").remove();
        $("#caida").append('<option style="display: none"></option>');
    }
    function districtDefault(){
        //$("#district option").remove();
        $('#district').val('');
    }
    function annexeDefault(){
        $("#annexe option").remove();
        $("#annexe").append('<option style="display: none"></option>');
    }
    function pashalikDefault(){
        $('#pashalik').val('');
    }
    function districtPashaslikCercleDefault(){
        $('#districtpashalik').val('');
    }


    divisionDefault();
    serviceDefault();
    cercleDefault();
    caidaDefault();
    districtDefault();
    annexeDefault();
    pashalikDefault();
    districtPashaslikCercleDefault();
    //entite

    function ajaxdivision(){
        if(selentite != null) {
            $("#division option").remove();
            $.ajax(
                {
                    type: "POST",
                    url: url6,
                    data: {entite: selentite.value},
                    success: function (data) {
                        $("#division").append(`<option value="" style="display: none" ></option>`);
                        for (var i = 0; i < data.divisions.length; i++) {
                            $("#division").append(`<option value="${data.divisions[i].iddivision}">${data.divisions[i].libelledivisionfr}</option>`);
                        }
                    }
                });
        }
    }

    if(selentite!=null) {
        selentite.onchange = function () {
            divisionDefault();
            serviceDefault();
            cercleDefault();
            caidaDefault();
            districtDefault();
            annexeDefault();
            pashalikDefault();
            districtPashaslikCercleDefault();
            districtPashaslikCercleDefault();
            if (selentite.value == "Secrétariat général") {
                frontivision();
                ajaxdivision();
            }else if(selentite.value == "Commandement"){
                    $(".districtpashalikdiv").show();
                    $(".divisiondiv").hide();
                    $(".pashalikdiv").hide();
                    $(".districtdiv").hide();
                    $(".annexediv").hide();
                    $(".servicediv").hide();

            }else if (selentite.value == "Dai" || selentite.value == "Cabinet" || selentite.value == "Dsic") {
                        frontivision();
                        ajaxdivision();
        }
    }

    //district
    const seldistrictpash= document.getElementById('districtpashalik');
    if(seldistrictpash != null) {
        seldistrictpash.onchange = function () {
            if (seldistrictpash.value == "District") {
                $(".divisiondiv").hide();
                $(".districtdiv").show();
                $(".pashalikdiv").hide();
                $(".servicediv").hide();
                $(".cerclediv").hide();
                $(".caidadiv").hide();
                divisionDefault();
                serviceDefault();
                cercleDefault();
                caidaDefault();
                districtDefault();
                annexeDefault();
                pashalikDefault();
            } else {

                if (seldistrictpash.value == "Pashalik") {
                    $(".divisiondiv").hide();
                    $(".districtdiv").hide();
                    $(".pashalikdiv").show();
                    $(".annexediv").hide();
                    $(".servicediv").hide();
                    $(".cerclediv").hide();
                    $(".caidadiv").hide();
                    divisionDefault();
                    serviceDefault();
                    cercleDefault();
                    caidaDefault();
                    districtDefault();
                    annexeDefault();
                    pashalikDefault();
                } else {
                    if (seldistrictpash.value == "Cercle") {
                        $(".divisiondiv").hide();
                        $(".districtdiv").hide();
                        $(".pashalikdiv").hide();
                        $(".annexediv").hide();
                        $(".servicediv").hide();
                        $(".cerclediv").show();
                        $(".caidadiv").hide();
                        divisionDefault();
                        serviceDefault();
                        cercleDefault();
                        caidaDefault();
                        districtDefault();
                        annexeDefault();
                        pashalikDefault();
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
        divisionDefault();
        serviceDefault();
        cercleDefault();
        caidaDefault();
        annexeDefault();
        pashalikDefault();
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
        divisionDefault();
        serviceDefault();
        caidaDefault();
        districtDefault();
        annexeDefault();
        pashalikDefault();
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
        serviceDefault();
        cercleDefault();
        caidaDefault();
        districtDefault();
        annexeDefault();
        pashalikDefault();
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
    if(sel != null) {
        sel.onchange = function () {

            $("#grade option").remove();
            $('#op1').remove()
            $.ajax(
                {
                    type: "POST",
                    url: url1,
                    data: {statutgrade: sel.value},
                    success: function (data) {
                        console.log(data)
                        $("#grade").append(`<option  style="display: none"></option>`);
                        for (var i = 0; i < data.grades.length; i++) {
                            $("#grade").append(`<option value="${data.grades[i].idgrade}">${data.grades[i].gradefr}</option>`);
                        }
                    }
                });
        }
    }



}
}