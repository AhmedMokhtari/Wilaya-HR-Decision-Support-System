window.onload = function (){

    selgrade = document.getElementById('grade')
    selnb = document.getElementById('nb')
    var jsondata;
    async function ajaxgrade(){
        $("#table tr").remove();
        $("#table1 tr").remove();
        $("#table2 tr").remove();
        $("#title center").remove();
        $("#title").append('<center><h3>  لائحة الترسيم والترقية الإستثنائية في الرتبة في درجة '+ selgrade.options[selgrade.selectedIndex].text+' لوزارة الداخلية</h3></center>')
       await $.ajax(
            {
                type: "POST",
                url: url1,
                data: {grade: selgrade.value, nb: selnb.value},
                success: function (data) {
                    $("#table tr").empty();
                    $("#table1 tr").empty();
                    $("#table2 tr").empty();
                    $("#title center").empty();
                    $("#title").append('<center><h3>  لائحة الترسيم والترقية الإستثنائية في الرتبة في درجة '+ selgrade.options[selgrade.selectedIndex].text+' لوزارة الداخلية</h3></center>')
                    console.log(data)
                    jsondata= data;
                    if(data.datawarehouse[0]!=null)
                    {
                        var inc = 0;
                         for (var i = 0; i < data.datawarehouse.length; i++) {
                             if (data.datawarehouse[i] != null) {
                                  inc ++;
                             }
                         }

                        $("#table1").append(`<tr><td>${selnb.value}</td></tr>`);
                        $("#table2").append(`<tr><td>10</td><td>10</td><td>${data.calcule.div}</td><td>${data.calcule.mod}</td><td>${data.calcule.div}</td></tr>`);
                    }
                    $("#linq a").attr("href","/avancement/pdfavencementexceptionnel?id="+selgrade.value+"&nb="+selnb.value+"&first="+data.calcule.div)
                    for (var i = 0; i < data.datawarehouse.length; i++) {
                        if(data.datawarehouse[i] != null)
                        {
                            $("#table").append(
                                `<tr><td>${data.datawarehouse[i].cin}</td>`+
                                `<td>${data.datawarehouse[i].personnelpar}</td>`+
                                `<td>${data.datawarehouse[i].personnelpfr}</td>`+
                                `<td>${data.datawarehouse[i].personnelnar}</td>`+
                                `<td>${data.datawarehouse[i].personnelnfr}</td>`+
                                `<td>${data.datawarehouse[i].ppr}</td>`+
                                `<td>${data.datawarehouse[i].echellondebut}</td>`+
                                `<td>${data.datawarehouse[i].indicesebut}</td>`+
                                `<td>${data.datawarehouse[i].datedebut}</td>`+
                                `<td>${data.datawarehouse[i].rythm}</td>`+
                                `<td>${data.datawarehouse[i].moyenne}</td>`+
                                `<td>${data.datawarehouse[i].echellondefin}</td>`+
                                `<td>${data.datawarehouse[i].indicesefin}</td>`+
                                `<td>${data.datawarehouse[i].datefin}</td>`+
                                `</tr>`);
                        }
                    }
                }
            });
    }
    ajaxgrade()
    selnb.addEventListener('input',ajaxgrade)
    selgrade.addEventListener('change',ajaxgrade)

    selpersonnels = document.getElementById('accept')
     function ajaxaccept(){
        $.ajax(
            {
                type: "POST",
                url: url2,
                data:JSON.stringify(jsondata),
                dataType: "json",
                success: function (response) {
                    console.log(response)
                    if(response == 'success')
                    {
                        alert('تمت المصادقة');
                    }
                }
            });
        alert('تمت المصادقة');
    }

    selpersonnels.addEventListener('click',ajaxaccept)
}
