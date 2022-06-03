
        //ajaxloadpersonnel
$(document).ready(function (){
    function loadadministration(){
        $("#personnel option").remove();
        $.ajax(
        {
            type:"POST",
            url: url7,
            data:{ administration: $('select[id=administration]').val()},
            success: function(data)
            {
                for(var i = 0; i < data.personnels.length; i++)
                {
                    $('select[id=personnel]').append(`<option value="${data.personnels[i].idpersonnel}">${data.personnels[i].cin}</option>`);
                }
                 loadpersonnel()
                console.log(data);
            }
        });
    }
    loadadministration()
    $('select[id=administration]').change(loadadministration);

    function loadpersonnel(){
        $("#table tr").remove();
        $.ajax(
        {
            type:"POST",
            url: url5,
            data:{ personnel: $('select[id=personnel]').val()},
            success: function(data)
            {
                $("#table").append(`<tr><th> الإسم الكامل :</th><td>${data.persodata.nomar} ${data.persodata.prenomar}</td></tr>'+
                                            '<tr><th>ب.ب.ر :</th><td>${data.persodata.ppr}</td></tr> <tr><th>  التعيين الحالي :</th><td>${data.persodata.oraganisme}</td></tr>'+
                                            '<tr><th>الرتبة :</th><td>${data.persodata.grade}</td></tr>`);



                if(data.persodata.reafectation!=null)
                {
                    $('#reaf').show();
                    $('#reafectationdonne').hide();
                    $('#reafectationbutton').hide();
                     $('#tablereaf').append(`<tr><th>  التعيين الجديد :</th><td>${data.persodata.reafectation[1]}</td></tr>'+
                            '<tr><th>المصادقة :</th><td><a class="btn btn-success" href="./addreaffectation/${data.persodata.idpersonnel}"><i class="fa-solid fa-check"></i></a></td></tr>`+
                            '<tr><th>إلغاء :</th><td><a class="btn btn-danger" href="./deletereaffectation/'+data.persodata.reafectation[0]+'"><i class="fa-solid fa-x"></i></a></td></tr>');

                }
                else {
                    $('#reafectationdonne').show();
                    $('#reafectationbutton').show();
                    $('#reaf').hide();
                }
            }
        });
    }

    $('select[id=personnel]').change(loadpersonnel);
})

