$(document).ready(function() {
    $(h_chart_id).highcharts({
        chart: h_chart,
        title: h_title,
        xAxis: h_xAxis,
        yAxis: h_yAxis,
        series: h_series,
        tooltip: {split: true,
            valueSuffix: ` ZAR`,
        },
        plotOptions: {spline: {
            marker: {enabled: false},
            pointInterval: 3600000,
            pointStart: Date.parse(`2019-09-03T12:04:00+0000`)}}
    });
});

