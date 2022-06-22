 document.getElementById('division').onchange = function (){
        $("#service option").remove();
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