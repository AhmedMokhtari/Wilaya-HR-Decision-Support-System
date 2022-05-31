    window.onload = function ()
    {
        / //ajaxloadpersonnel
        const selpersonnel = document.getElementById('personnel');
        $('select[id=personnel]').change(function (){
            $("#table tr").remove();
            $.ajax(
            {
                type:"POST",
                url: url5,
                data:{ personnel: $('select[id=personnel]').val()},
                success: function(data)
                {
                    $("#table").append(`<tr><th> الإسم الكامل :</th><td>${data.persodata.nomar} ${data.persodata.prenomar[0]}</td></tr>'+
                                                '<tr><th>ب.ب.ر :</th><td>${data.persodata.ppr}</td></tr> <tr><th>  التعيين الحالي :</th><td>${data.persodata.oraganisme}</td></tr>'+
                                                '<tr><th>الرتبة :</th><td>${data.persodata.grade}</td></tr>`);
                    console.log(data);
                }
            });
        });

    }