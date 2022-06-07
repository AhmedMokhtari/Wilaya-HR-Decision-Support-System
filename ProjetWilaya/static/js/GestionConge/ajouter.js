window.onload = loadpersonnel()

function loadpersonnel(){
    $("#table tr").remove();

    $.ajax(
    {
        type:"POST",
        url: url5,
        async: false,
        data: { personnel: document.getElementById('personneldata').value},
        success: function(data)
        {
            console.log(data)
            if(data.persodata != "")
            {

                $("#table").append(`<tr><th> الإسم الكامل :</th><td>${data.persodata[0].nomar} ${data.persodata[0].prenomar}</td></tr>'+
                                        '<tr><th>ر.ب.و :</th><td>${data.persodata[0].cin}</td></tr><tr><th>رقم التأجير :</th><td>${data.persodata[0].ppr}</td></tr> <tr><th>الجنس :</th><td>${data.persodata[0].sexe}</td></tr> <tr><th>  رخصة إدارية :</th><td id="congean">${data.congean}</td></tr>'+
                                        '<tr id="homme"><th>رخصة الأبوة :</th><td id="congeparen">${data.congeparen}</td></tr><tr id="femme"><th>رخصة الأمومة :</th><td id="congemere">${data.congemere}</td></tr><tr><th>رخصة إستثنائية :</th><td id="congestit">${data.congestit}</td></tr>'+
                                         '<tr><th>رخصة الحج :</th><td id="congehaj">${data.congehaj}</td></tr>`);

                if(data.persodata[0].sexe === 'Homme-ذكر')
                {
                    $('#homme').show();
                    $('#femme').hide();
                    $('#femmeop').remove();

                }
                else
                {
                    if(data.persodata[0].sexe === 'Femme-أنثى')
                    {
                        $('#homme').hide();
                        $('#hommeop').remove();
                        $('#femme').show();

                    }
                }

                if(data.congehaj >= 40)
                {
                    $('#congehaj').css("color","red")
                }

                if(data.congemere >= 98)
                {
                    $('#congemere').css("color","red")
                }

                if(data.congean >= 44)
                {
                    $('#congean').css("color","red")
                }

                if(data.congeparen >= 14)
                {
                    $('#congeparen').css("color","red")
                }

                if(data.congestit >= 14)
                {
                    $('#congestit').css("color","red")
                }




                sessionStorage.clear();
                sessionStorage.setItem('congehaj', data.congehaj);
                sessionStorage.setItem('congemere', data.congemere);
                sessionStorage.setItem('congestit', data.congestit);
                sessionStorage.setItem('congeparen', data.congeparen);
                sessionStorage.setItem('congean', data.congean);
                sessionStorage.setItem('personnelresponse', 'true');
            }
            else
            {
                if(data.persodata == ""){
                    $("#table").append(`<tr><th> الإسم الكامل :</th><td></td></tr>'+
                                        '<tr><th>ر.ب.و :</th><td></td></tr><tr><th>رقم التأجير :</th><td></td></tr> <tr><th>  رخصة إدارية :</th><td></td></tr>'+
                                        '<tr><th>رخصة الأبوة :</th><td></td></tr><th>رخصة الأمومة :</th><td></td></tr><tr><th>رخصة إستثنائية :</th><td></td></tr>'+
                                        '<tr><th>رخصة الحج :</th><td></td></tr>`);

                    sessionStorage.clear();
                    sessionStorage.setItem('personnelresponse', 'false');
                }

            }

        }

    });
}










