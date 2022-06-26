window.onload = function () {
    selanneeorga = document.getElementById('anneeorga')
     function ajaxload(){
        $.ajax(
            {
                type: "POST",
                url: url1,
                data: {anneeorga : selanneeorga.value},
                dataType: "json",
                success: function (response) {
                    console.log(response)
                }
            });
    }

    selpersonnels.addEventListener('click',ajaxload)
}