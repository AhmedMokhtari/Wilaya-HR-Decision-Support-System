/*document.querySelectorAll('input[type=file]').forEach(item =>{
    item.addEventListener('change',function (e){
        let div = document.querySelector('.inp');
        div.innerHTML = '<input type="text" class="form-control" value=`${item.value}`>'
    })
})*/

window.onload = function () {
    var divisions = document.getElementById('division');

    divisions.onchange = function (){
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
}