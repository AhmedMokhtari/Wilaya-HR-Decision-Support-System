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

                $("#table").append(`<tr><th> الإسم الكامل :</th><td id="testdata">${data.persodata[0].nomar} ${data.persodata[0].prenomar}</td></tr>'+
                                        '<tr><th>ر.ب.و :</th><td>${data.persodata[0].cin}</td></tr><tr><th>رقم التأجير :</th><td>${data.persodata[0].ppr}</td></tr> <tr><th>  رخصة إدارية :</th><td>${data.congean}</td></tr>'+
                                        '<tr><th>الرخصة الأبوة :</th><td>${data.congeparen}</td></tr><th>رخصة الأمومة :</th><td>${data.congemere}</td></tr><tr><th>رخصة إستثنائية :</th><td>${data.congestit}</td></tr>'+
                                         '<tr><th>رخصة الحج :</th><td>${data.congehaj}</td></tr>`);

                sessionStorage.setItem('personnelresponse', 'true');
            }
            else
            {
                if(data.persodata == ""){
                    $("#table").append(`<tr><th> الإسم الكامل :</th><td></td></tr>'+
                                        '<tr><th>ر.ب.و :</th><td></td></tr><tr><th>رقم التأجير :</th><td></td></tr> <tr><th>  رخصة إدارية :</th><td></td></tr>'+
                                        '<tr><th>الرخصة الأبوة :</th><td></td></tr><th>رخصة الأمومة :</th><td></td></tr><tr><th>رخصة إستثنائية :</th><td></td></tr>'+
                                        '<tr><th>رخصة الحج :</th><td></td></tr>`);

                    sessionStorage.setItem('personnelresponse', 'false');
                }

            }

        }

    });
}










