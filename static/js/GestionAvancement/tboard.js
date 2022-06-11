window.onload = function (){

    selgrade = document.getElementById('grade')

     function ajaxgrade(){
        $("#table tr").remove();
        $("#title center").remove();
        $("#title").append('<center><h3>  لائحة الترسيم والترقية في الرتبة في درجة '+ selgrade.options[selgrade.selectedIndex].text+' لوزارة الداخلية</h3></center>')
        $.ajax(
            {
                type: "POST",
                url: url1,
                data: {grade: selgrade.value},
                success: function (data) {
                    console.log(data)

                    for (var i = 0; i < data.length; i++) {

                        $("#table").append(`<tr><td>${data[i].cin}</td>`+
                            `<td>${data[i].personnelpar}</td>`+
                            `<td>${data[i].personnelpfr}</td>`+
                            `<td>${data[i].personnelnar}</td>`+
                            `<td>${data[i].personnelnfr}</td>`+
                            `<td>${data[i].ppr}</td>`+
                            `<td>${data[i].echellondebut}</td>`+
                            `<td>${data[i].indicesebut}</td>`+
                            `<td>${data[i].datedebut}</td>`+
                            `<td>${data[i].rythm}</td>`+
                            `<td>${data[i].moyenne}</td>`+
                            `<td>${data[i].echellondefin}</td>`+
                            `<td>${data[i].indicesefin}</td>`+
                            `<td>${data[i].datefin}</td>`+
                            `</tr>`);
                    }
                }
            });
    }
    ajaxgrade()
    selgrade.addEventListener('change',ajaxgrade)


}
