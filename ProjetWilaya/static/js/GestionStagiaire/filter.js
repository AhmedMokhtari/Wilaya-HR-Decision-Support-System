
document.getElementById('formsearch').addEventListener('change',function (e){
            let division=$('#division');
            let service=$('#service');
          if(e.target.getAttribute('name')=='radioGenre' || e.target.getAttribute('name')== 'statut') {
              let state = document.getElementById('statut').value;
              let radioval = $('input[name=radioGenre]:checked', '#formsearch').val()
              if (division.val() != '') {
                  if (service.val() != '') {
                      console.log('filter service')
                      let val = service.getAttribute('name') + '&' + service.val() + '&' + radioval + '&' + state;
                      ajaxstage(val)

                  } else {
                      let val = division.attr("name") + '&' + division.val() + '&' + radioval + '&' + state;
                      ajaxstage(val)
                  }
              } else {
                  let val = 'All&All&' + radioval + '&' + state;
                  ajaxstage(val)
              }
          }
          else {
            let state=document.getElementById('statut').value;
            let radioval=$('input[name=radioGenre]:checked', '#formsearch').val()
            let val= e.target.getAttribute('name') +'&'+e.target.value+'&'+radioval+'&'+state;
            ajaxstage(val)
          }
      })

 function ajaxstage(object){
    let table=$('#table').DataTable()
    table.clear().draw();
    $.ajax({
        type: 'get',
        url: `stage-json/${object}/`,
        success: function(response){
            const stagedata = response.data
            //let tb1 = document.querySelector('#tbody');
           // tb1.innerHTML=""
          dataa=JSON.parse(stagedata);
          console.log(dataa);
          dataa.forEach(item=>{
                let table =$('#table').DataTable();
                let idp = item.stage.idstage;
                let statut = ''
                if (item.statut == 'Pas commencer')
                    statut = `<span class="badge badge-primary p-2">${item.statut}</span>`
                if (item.statut == 'En cours')
                    statut = `<span class="badge badge-warning p-2">${item.statut}</span>`
                if (item.statut == 'Terminé')
                    statut = `<span class="badge badge-success p-2">${item.statut}</span>`
                table.row.add([
                    item.stage.cin ,
                    item.stage.nomstagiairear+' '+item.prenomstagiairear,
                    item.stage.nomstagiairefr+" "+item.prenomstagiairefr,
                    item.stage.sexe,
                    item.stage.idservice_field__iddivision_field__libelledivisionfr,
                    item.stage.idservice_field__libelleservicefr,
                    statut,
                   `<a href="/infos/${idp}" class="btn btn-success m-1"><i class="fa-solid fa-arrow-up-right-from-square fa-lg " ></i></a><a href="/infos/${idp}"class="btn btn-warning btn-icon  mx-1"><i class="fa-solid fa-pen-to-square fa-lg"></i></a>`
                ]).draw();
            })
        },
        error: function(error){
            console.log(error)
        }
    })
}


window.onload = function () {
    console.log(document.getElementById('statut').value);
        var divisions = document.getElementById('division');

        function serviceDefault() {
            $("#service option").remove();
            $("#service").append('<option style="display: none"></option>');
        }

        if (divisions != null) {
            $('.servicediv').hide()
        }

        serviceDefault()
        divisions.onchange = function (){
            $(".servicediv").show();
            $("#service option").remove();
            serviceDefault();
            $.ajax(
            {
                type:"POST",
                url: url0,
                data:{ division: division.value},
                success: function(data)
                {
                    for(var i = 0; i < data.services.length; i++)
                    {
                        $("#service").append(`<option value="${data.services[i].idservice}">${data.services[i].libelleservicefr}</option>`);

                    }
                }
            });
        }
}