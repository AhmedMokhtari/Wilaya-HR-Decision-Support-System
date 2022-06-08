window.onload = function (){
    selgrade = document.getElementById('grade')
    function ajaxgrade(){
    if(selgrade != null) {
        $("#table tr").remove();
        $.ajax(
            {
                type: "POST",
                url: url1,
                data: {grade: selgrade.value},
                success: function (data) {
                    console.log(data)
                    for (var i = 0; i < data.personnels.length; i++) {
                        $("#table").append(`<tr><td>${data.personnels[i]}</td></tr>`);
                    }
                }
            });
    }
    selgrade.addEventListener('change', ajaxgrade)
}
}
