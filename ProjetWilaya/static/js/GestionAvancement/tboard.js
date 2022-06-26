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
                    google.charts.load('current', {'packages':['corechart']});
                      google.charts.setOnLoadCallback(drawVisualization);

                      function drawVisualization() {
                        // Some raw data (not necessarily accurate)
                        var data = google.visualization.arrayToDataTable([
                          ['الشهر', 'المصلحة', 'الباشوية', 'الدائرة', 'الملحقة', 'القيادة', '-'],
                          ['2018',  65,      38,         22,              98,           50,      14.6],
                          ['2019',  35,      120,        99,             268,           88,      82],
                          ['2020',  57,      167,        87,              7,           97,      23],
                          ['2021',  39,      110,        15,              68,           15,      9.4],
                          ['2022',  36,      91,         29,             26,           66,      69.6]
                        ]);

                        var options = {
                          title : 'عدد المترقين في الهيئات',
                          vAxis: {title: 'الموضفون'},
                          hAxis: {title: 'الأشهر'},
                          seriesType: 'bars',
                          series: {5: {type: 'line'}}
                        };

                        var chart = new google.visualization.ComboChart(document.getElementById('chart_div1'));
                        chart.draw(data, options);
                      }
                }
            });
    }
    ajaxload()
    selanneeorga.addEventListener('click',ajaxload)
}