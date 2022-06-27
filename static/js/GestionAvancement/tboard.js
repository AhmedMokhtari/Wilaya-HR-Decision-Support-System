window.onload = function () {
    var selanneeorga = document.getElementById('anneeorga')
     function ajaxload(){
        $.ajax(
            {
                type: "POST",
                url: url1,
                data: {anneeorga : selanneeorga.value},
                dataType: "json",
                success: function (response) {
                    console.log(response)
                    if(selanneeorga.value==2)
                    {
                        google.charts.load('current', {'packages':['corechart']});
                        google.charts.setOnLoadCallback(drawVisualization);

                        function drawVisualization()
                        {
                            // Some raw data (not necessarily accurate)
                            var data = google.visualization.arrayToDataTable([
                              ['السنة', 'المصلحة', 'الباشوية',  'الملحقة', 'القيادة', '-'],
                              [ response[0].Annee.toString(),  response[0].service, response[0].pashalik,  response[0].annexe, response[0].caidat, 0],
                              [ response[1].Annee.toString(),  response[1].service, response[1].pashalik,  response[1].annexe, response[1].caidat, 0],
                              [ response[2].Annee.toString(),  response[2].service, response[2].pashalik,  response[2].annexe, response[2].caidat, 0],
                              [ response[3].Annee.toString(),  response[3].service, response[3].pashalik,  response[3].annexe, response[3].caidat, 0],
                              [ response[4].Annee.toString(),  response[4].service, response[4].pashalik,  response[4].annexe, response[4].caidat, 0],
                            ]);

                            var options = {
                              title : 'عدد المترقين في الهيئات',
                              vAxis: {title: 'الموضفون'},
                              hAxis: {title: 'السنوات'},
                              seriesType: 'bars',
                              series: {5: {type: 'line'}}
                            };

                            var chart = new google.visualization.ComboChart(document.getElementById('chart_div1'));
                            chart.draw(data, options);
                        }
                    }
                    else
                    {
                        google.charts.load('current', {'packages':['corechart']});
                        google.charts.setOnLoadCallback(drawVisualization);

                        function drawVisualization()
                        {
                            // Some raw data (not necessarily accurate)
                            var data = google.visualization.arrayToDataTable([
                              ['السنة', 'المصلحة', 'الباشوية', 'الملحقة', 'القيادة', '-'],
                              [ response[0].Annee.toString(),  response[0].service, response[0].pashalik, response[0].annexe, response[0].caidat, 0],
                              [ response[1].Annee.toString(),  response[1].service, response[1].pashalik, response[1].annexe, response[1].caidat, 0],
                            ]);

                            var options = {
                              title : 'عدد المترقين في الهيئات',
                              vAxis: {title: 'الموضفون'},
                              hAxis: {title: 'السنوات'},
                              seriesType: 'bars',
                              series: {5: {type: 'line'}}
                            };

                            var chart = new google.visualization.ComboChart(document.getElementById('chart_div1'));
                            chart.draw(data, options);
                        }
                    }
                }
            });
    }
    ajaxload()
    selanneeorga.addEventListener('change',ajaxload)


    var selannee = document.getElementById('annee')
     function ajaxloadannee()
     {

        $.ajax(
            {
                type: "POST",
                url: url2,
                data: {annee: selannee.value},
                success: function (response) {
                    console.log(response)
                    if(selannee.value==2)
                    {
                            google.charts.load('current', {'packages':['corechart']});
                            google.charts.setOnLoadCallback(drawChart);
                          function drawChart()
                          {
                            var data = google.visualization.arrayToDataTable([
                              ['السنة', 'الترقية العادية', 'الترقية الإستثنائية'],
                                [response[0].Annee.toString(),response[0].countNormal,response[0].countExcep],
                                [response[1].Annee.toString(),response[1].countNormal,response[1].countExcep],
                                [response[2].Annee.toString(),response[2].countNormal,response[2].countExcep],
                                [response[3].Annee.toString(),response[3].countNormal,response[3].countExcep],
                            ]);

                            var options = {
                              title: 'عدد المترقين في السنة',
                              hAxis: {title: 'السنة',  titleTextStyle: {color: '#333'}},
                              vAxis: {minValue: 0, title: 'الموضفون'}
                            };

                            var chart = new google.visualization.AreaChart(document.getElementById('chart_div'));
                            chart.draw(data, options);
                          }
                    }
                    else
                    {
                        google.charts.load('current', {'packages':['corechart']});
                            google.charts.setOnLoadCallback(drawChart);
                          function drawChart()
                          {
                            var data = google.visualization.arrayToDataTable([
                              ['السنة', 'الترقية العادية', 'الترقية الإستثنائية'],
                                [response[0].Annee.toString(),response[0].countNormal,response[0].countExcep],
                                [response[1].Annee.toString(),response[1].countNormal,response[1].countExcep],
                            ]);

                            var options = {
                              title: 'عدد المترقين في السنة',
                              hAxis: {title: 'السنة',  titleTextStyle: {color: '#333'}},
                              vAxis: {minValue: 0, title: 'الموضفون'}
                            };

                            var chart = new google.visualization.AreaChart(document.getElementById('chart_div'));
                            chart.draw(data, options);
                          }
                    }
                }
            });
    }
    ajaxloadannee()
    selannee.addEventListener('change',ajaxloadannee)
}