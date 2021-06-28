$(document).ready(function () {
    $('.chart_select_radio_label').change((e) => {
        var st = $('input:radio[name="chart_sel_radio"]:checked').val()
        setSelectChartAction(getSelectChartIndex())
        selectChartType(st)
    });
});

const getSelectChartIndex = () => {
    $("input[name='chart_sel_radio']:checked").each((i, elmt) => {
        index = $(elmt).index("input[name='chart_sel_radio']");
    });

    return index;
};

const setSelectChartAction = (index) => {
    $('.chart_select_radio_label').each((i, elmt) => {
        $(elmt).css('opacity', i === index ? '1.0' : '0.3');
        $(elmt).css('font-weight', i === index ? 'bold' : 'unset');
    });
};

const selectChartType = (chartType) => {
    switch (chartType) {
        case 'bar3d':
            $('#bar_chart_3d_3').css('display', 'flex');
            $('#bar_chart_3').css('display', 'none');
            $('#spiderweb_chart_3').css('display', 'none');
            $('#bar_chart_3d_4').css('display', 'flex');
            $('#bar_chart_4').css('display', 'none');
            $('#spiderweb_chart_4').css('display', 'none');
            break;
        case 'bar':
            $('#bar_chart_3d_3').css('display', 'none');
            $('#bar_chart_3').css('display', 'flex');
            $('#spiderweb_chart_3').css('display', 'none');
            $('#bar_chart_3d_4').css('display', 'none');
            $('#bar_chart_4').css('display', 'flex');
            $('#spiderweb_chart_4').css('display', 'none');
            break;
        case 'spiderweb':
            $('#bar_chart_3d_3').css('display', 'none');
            $('#bar_chart_3').css('display', 'none');
            $('#spiderweb_chart_3').css('display', 'flex');
            $('#bar_chart_3d_4').css('display', 'none');
            $('#bar_chart_4').css('display', 'none');
            $('#spiderweb_chart_4').css('display', 'flex');
            break;
    }
};

function draw_warm_box(val, standard_val) {
    if (standard_val == "1") {
        gap = 0.2;
    } else {
        gap = 0.1;
    }

    if (val >= standard_val - gap && val <= standard_val + gap) {
        // 정상 범주
        return [
            {
                id: "box1",
                type: "box",
                yScaleID: "y-axis-1",
                yMin: standard_val - gap,
                yMax: standard_val + gap,
                backgroundColor: "rgba(100, 100, 100, 0.2)",
                borderColor: "rgba(100, 100, 100, 0.3)",
            },
        ];
    } else {
        re_val = [
            {
                id: "box1",
                type: "box",
                yScaleID: "y-axis-1",
                yMin: -10,
                yMax: standard_val - gap,
                backgroundColor: "rgba(200, 100, 200, 0.08)",
                borderColor: "rgba(200, 100, 200, 0.1)",
            },
            {
                id: "box2",
                type: "box",
                yScaleID: "y-axis-1",
                yMin: standard_val - gap,
                yMax: standard_val + gap,
                backgroundColor: "rgba(100, 100, 100, 0.2)",
                borderColor: "rgba(100, 100, 100, 0.3)",
            },
            {
                id: "box3",
                type: "box",
                yScaleID: "y-axis-1",
                yMin: standard_val + gap,
                yMax: 10,
                backgroundColor: "rgba(200, 100, 200, 0.08)",
                borderColor: "rgba(200, 100, 200, 0.1)",
            },
        ];
        return re_val;
    }
}

function draw_cool_box(val, standard_val) {
    if (standard_val == "1") {
        gap = 0.2;
    } else {
        gap = 0.1;
    }

    if (val >= standard_val - gap && val <= standard_val + gap) {
        // 정상 범주
        return [
            {
                id: "box1",
                type: "box",
                yScaleID: "y-axis-1",
                yMin: standard_val - gap,
                yMax: standard_val + gap,
                backgroundColor: "rgba(100, 100, 100, 0.2)",
                borderColor: "rgba(100, 100, 100, 0.3)",
            },
        ];
    } else {
        re_val = [
            {
                id: "box1",
                type: "box",
                yScaleID: "y-axis-1",
                yMin: -10,
                yMax: standard_val - gap,
                backgroundColor: "rgba(222, 237, 201, 0.2)",
            },
            {
                id: "box2",
                type: "box",
                yScaleID: "y-axis-1",
                yMin: standard_val - gap,
                yMax: standard_val + gap,
                backgroundColor: "rgba(100, 100, 100, 0.2)",
                borderColor: "rgba(100, 100, 100, 0.3)",
            },
            {
                id: "box3",
                type: "box",
                yScaleID: "y-axis-1",
                yMin: standard_val + gap,
                yMax: 10,
                backgroundColor: "rgba(222, 237, 201, 0.2)",
                borderColor: "rgba(200, 100, 200, 0.1)",
            },
        ];
        return re_val;
    }
}

function make_option(val, standard_val, title, chk, color) {
    if (chk) {
        if (color == "warm") {
            annotation_val = {
                drawTime: "afterDraw",
                annotations: draw_warm_box(val, standard_val),
            };
        } else {
            annotation_val = {
                drawTime: "afterDraw",
                annotations: draw_cool_box(val, standard_val),
            };
        }
    } else {
        annotation_val = {};
    }

    return {
        maintainAspectRatio: false,
        cutoutPercentage: 50,
        responsive: true,
        legend: {
            position: "bottom",
        },
        title: {
            display: true,
            text: title,
        },
        scales: {
            yAxes: [
                {
                    id: "y-axis-1",
                    ticks: {
                        beginAtZero: true,
                        suggestedMax: 1,
                    },
                },
            ],
            xAxes: [
                {
                    barPercentage: 0.5,
                },
            ],
        },
        annotation: annotation_val,
        plugins: {
            datalabels: {
                align: "end",
                anchor: "end",
                borderRadius: 4,
                padding: {
                    bottom: 1,
                },
                formatter: function (value) {
                    return value;
                },
            },
        },
    };
}

function rate_cal(before, after, target) {
    abs_mitigate_rate = Math.abs(target - after) / Math.abs(target - before);

    if (abs_mitigate_rate > 1) return -abs_mitigate_rate * 100;
    else return (1 - abs_mitigate_rate) * 100;
}

function two_bar_warm_dataset(data1, data2) {
    return [
        {
            label: "original",
            backgroundColor: "rgba(255, 94, 0, 0.5)",
            borderWidth: 0,
            data: [data1],
        },
        {
            label: "mitigated",
            backgroundColor: "rgba(255, 0, 0, 0.5)",
            borderWidth: 0,
            data: [data2],
        },
    ];
}

function two_bar_cool_dataset(data1, data2) {
    return [
        {
            label: "original",
            backgroundColor: "rgba(156, 199, 93, 0.5)",
            borderWidth: 0,
            data: [data1],
        },
        {
            label: "mitigated",
            backgroundColor: "rgba(18, 154, 144, 0.5)",
            borderWidth: 0,
            data: [data2],
        },
    ];
}

/**
 * draw_column_graph 함수를 통해 그릴 데이터를 분리해 반환합니다.
 * 앞에 다섯 데이터는 originalData 뒤의 다섯 데이터는 mitigatedData 로 반환합니다.
 * @param {object} data
 * @returns {object} {originalData: [], mitigatedData: []}
 */
function split_data_for_graph(data) {
    return {
        originalData: data.slice(0, 5),
        mitigatedData: data.slice(5, 10),
    };
}

/**
 * original, mitigated 데이터들에 대한 성별, 인종 그래프 그리기
 */
function draw_3d_column_graph(
    renderTo,
    title,
    subtitle,
    originalData,
    mitigatedData
) {
    Highcharts.chart({
        chart: {
            renderTo,
            type: "column",
            options3d: {
                enabled: true,
                alpha: 15,
                beta: 20,
                depth: 200,
                viewDistance: 100,
            },
        },
        title: {
            text: title,
        },
        subtitle: {
            text: subtitle,
        },
        plotOptions: {
            column: {
                depth: 100,
                groupZPadding: 0,
                grouping: false,
                pointWidth: 80,
            },
            series: {
                pointPadding: 0,
                groupPadding: 0,
            },
        },
        xAxis: {
            categories: [
                "Statistical Parity Difference",
                "Disparate impact",
                "Equal opportunity difference",
                "Average odds difference",
                "Theil index",
            ],
            offset: 20,
        },
        yAxis: {
            title: {
                enabled: false,
            },
            tickInterval: 0.25,
        },
        zAxis: {
            min: 0,
            max: 3,
            categories: ["", "original", "mitigated", ""],
            labels: {
                rotation: 20,
                y: 30,
            },
        },
        series: [
            {
                stack: 0,
                name: "original",
                data: originalData,
                color: "#FF0000bb",
            },
            {
                stack: 1,
                name: "mitigated",
                data: mitigatedData,
            },
        ],
    });
}

function draw_column_graph(
    renderTo,
    title,
    subtitle,
    originalData,
    mitigatedData
) {
    Highcharts.chart({
        chart: {
            renderTo,
            type: 'column'
        },
        title: {
            text: title,
        },
        subtitle: {
            text: subtitle,
        },
        xAxis: {
            categories: [
                "Statistical Parity Difference",
                "Disparate impact",
                "Equal opportunity difference",
                "Average odds difference",
                "Theil index",
            ]
        },
        yAxis: {
            title: {
                enabled: false,
            },
        },
        credits: {
            enabled: false
        },
        series: [{
            name: 'original',
            data: originalData,
            color: "#FF0000bb",
        }, {
            name: 'mitigated',
            data: mitigatedData
        }]
    });
}

function draw_spiderweb_graph(
    renderTo,
    title,
    subtitle,
    originalData,
    mitigatedData
) {
    Highcharts.chart({
        chart: {
            renderTo,
            polar: true,
            type: 'line'
        },
        title: {
            text: title,
        },
        subtitle: {
            text: subtitle,
        },
        pane: {
            size: '90%'
        },

        xAxis: {
            categories: [
                "Statistical Parity Difference",
                "Disparate impact",
                "Equal opportunity difference",
                "Average odds difference",
                "Theil index",
            ],
            tickmarkPlacement: 'on',
            lineWidth: 0,
        },

        yAxis: {
            gridLineInterpolation: 'polygon',
            lineWidth: 0,
        },

        tooltip: {
            shared: true,
            pointFormat: '<span style="color:{series.color}">{series.name}: <b>{point.y:,.2f}</b><br/>'
        },

        legend: {
            align: 'right',
            verticalAlign: 'middle',
            layout: 'vertical'
        },

        series: [{
            name: 'original',
            data: originalData,
            pointPlacement: 'on',
            color: "#FF0000bb",
        }, {
            name: 'mitigated',
            data: mitigatedData,
            pointPlacement: 'on'
        }],

        responsive: {
            rules: [{
                condition: {
                    maxWidth: 500
                },
                chartOptions: {
                    legend: {
                        align: 'center',
                        verticalAlign: 'bottom',
                        layout: 'horizontal'
                    },
                    pane: {
                        size: '90%'
                    }
                }
            }]
        }
    });
}

if (window.location.pathname == "/compare") {
    $.ajax({
        url: "after_chart_data",
        type: "POST",
        data: { msg: "test" },
        dataType: "JSON",
        contentType: "application/json",
        success: function (result) {
            // ajax 성공시 로딩숨기고 차트 보여주기
            $("#loading_div").hide();
            $("#chart_content").show();

            tsen_xy_data = result["tsen_xy_data"];
            pca_xy_data = result["pca_xy_data"];
            aif_value1 = result["aif_value1"]; // 0~4 before, 5~9 after
            aif_value2 = result["aif_value2"];
            protect = result["protect"];

            console.group("getjson")
            console.log("tsen_xy_data : ", tsen_xy_data)
            console.log("pca_xy_data : ", pca_xy_data)
            console.log("aif_value1 : ", aif_value1)
            console.log("aif_value2 : ", aif_value2)
            console.log("protect : ", protect)
            console.groupEnd()

            $(".protect-attribute-key.group-one").text(protect[0]);
            $(".protect-attribute-val.group-one").text(protect[1]);
            $(".protect-attribute-key.group-two").text(protect[2]);
            $(".protect-attribute-val.group-two").text(protect[3]);

            /*scatter chart*/
            let value_one_AccuracyText = "Accuracy after mitigation unchanged";
            if (aif_value1.length > 10) {
                value_one_AccuracyText = `Accuracy after mitigation changed from ${String((aif_value1[10] * 100).toFixed(2)) + "%"
                    } to ${String((aif_value1[11] * 100).toFixed(2)) + "%"}`;
            }
            $(".value_one_accuracy_text").text(value_one_AccuracyText);

            let value_two_AccuracyText = "Accuracy after mitigation unchanged";
            if (aif_value2.length > 10) {
                value_two_AccuracyText = `Accuracy after mitigation changed from ${String((aif_value2[10] * 100).toFixed(2)) + "%"
                    } to ${String((aif_value2[11] * 100).toFixed(2)) + "%"}`;
            }
            $(".value_two_accuracy_text").text(value_two_AccuracyText);

            // 1
            var protect_value_1 = [];
            // 0
            var protect_other_1 = [];

            // 1
            var protect_value_2 = [];

            // 0
            var protect_other_2 = [];
            for (var i = 0; i < tsen_xy_data.length; i++) {
                var tsen_xy = tsen_xy_data[i];
                var tmp_data = [];
                tmp_data.push(tsen_xy[0]);
                tmp_data.push(tsen_xy[1]);
                if (tsen_xy[2] == 1) {
                    protect_value_1.push(tmp_data);
                } else {
                    protect_other_1.push(tmp_data);
                }

                if (tsen_xy[3] == 1) {
                    protect_value_2.push(tmp_data);
                } else {
                    protect_other_2.push(tmp_data);
                }
            }

            // T-SNE Algorithm 그래프
            Highcharts.chart({
                chart: {
                    renderTo: "scatter_container1",
                    type: "scatter",
                    zoomType: "xy",
                },
                accessibility: {
                    description: "",
                },
                title: {
                    text: "T-SNE algorithm(" + protect[0] + ")",
                },
                subtitle: {
                    text: "",
                },

                legend: {
                    layout: "vertical",
                    align: "left",
                    verticalAlign: "top",
                    x: 100,
                    y: 70,
                    floating: true,
                    backgroundColor:
                        Highcharts.defaultOptions.chart.backgroundColor,
                    borderWidth: 1,
                },
                plotOptions: {
                    scatter: {
                        marker: {
                            radius: 5,
                            states: {
                                hover: {
                                    enabled: true,
                                    lineColor: "rgb(100,100,100)",
                                },
                            },
                        },
                        states: {
                            hover: {
                                marker: {
                                    enabled: false,
                                },
                            },
                        },
                        tooltip: {
                            headerFormat: "<b>{series.name}</b><br>",
                            pointFormat: "{point.x} , {point.y} ",
                        },
                    },
                },
                series: [
                    {
                        name: protect[1],
                        type: "scatter",
                        color: "rgba(129, 199, 233, 0.2)",
                        data: protect_value_1,
                    },
                    {
                        name: "other",
                        type: "scatter",
                        color: "rgba(255, 187, 0, 0.2)",
                        data: protect_other_1,
                    },
                ],
            });

            Highcharts.chart("scatter_container2", {
                chart: {
                    type: "scatter",
                    zoomType: "xy",
                },
                accessibility: {
                    description: "",
                },
                title: {
                    text: "T-SNE algorithm(" + protect[2] + ")",
                },
                subtitle: {
                    text: "",
                },

                legend: {
                    layout: "vertical",
                    align: "left",
                    verticalAlign: "top",
                    x: 100,
                    y: 70,
                    floating: true,
                    backgroundColor:
                        Highcharts.defaultOptions.chart.backgroundColor,
                    borderWidth: 1,
                },
                plotOptions: {
                    scatter: {
                        marker: {
                            radius: 5,
                            states: {
                                hover: {
                                    enabled: true,
                                    lineColor: "rgb(100,100,100)",
                                },
                            },
                        },
                        states: {
                            hover: {
                                marker: {
                                    enabled: false,
                                },
                            },
                        },
                        tooltip: {
                            headerFormat: "<b>{series.name}</b><br>",
                            pointFormat: "{point.x} , {point.y} ",
                        },
                    },
                },
                series: [
                    {
                        name: protect[3],
                        color: "rgba(128, 65, 217, 0.2)",
                        data: protect_value_2,
                    },
                    {
                        name: "other",
                        color: "rgba(0, 255, 0, 0.2)",
                        data: protect_other_2,
                    },
                ],
            });

            // Sex, Race mitigation 그래프
            const {
                originalData: aifOriginalData1,
                mitigatedData: aifMitigatedData1,
            } = split_data_for_graph(aif_value1);
            const {
                originalData: aifOriginalData2,
                mitigatedData: aifMitigatedData2,
            } = split_data_for_graph(aif_value2);
            draw_3d_column_graph(
                "bar_chart_3d_3",
                "",
                "",
                aifOriginalData1,
                aifMitigatedData1
            );

            draw_3d_column_graph(
                "bar_chart_3d_4",
                "",
                "",
                aifOriginalData2,
                aifMitigatedData2
            );

            draw_column_graph(
                "bar_chart_3",
                "",
                "",
                aifOriginalData1,
                aifMitigatedData1
            )

            draw_column_graph(
                "bar_chart_4",
                "",
                "",
                aifOriginalData2,
                aifMitigatedData2
            )

            draw_spiderweb_graph(
                "spiderweb_chart_3",
                "",
                "",
                aifOriginalData1,
                aifMitigatedData1
            )

            draw_spiderweb_graph(
                "spiderweb_chart_4",
                "",
                "",
                aifOriginalData2,
                aifMitigatedData2
            )

            //            $(".highcharts-legend").remove();
            $(".highcharts-exporting-group").remove();
            $("button").eq(3).remove();
            $("button").eq(2).remove();

            /* radar chart*/
            mitigate_rate_value_one = [
                rate_cal(aif_value1[0], aif_value1[5], 0),
                rate_cal(aif_value1[1], aif_value1[6], 1),
                rate_cal(aif_value1[2], aif_value1[7], 0),
                rate_cal(aif_value1[3], aif_value1[8], 0),
            ];
            console.log('one', mitigate_rate_value_one)

            mitigate_rate_value_two = [
                rate_cal(aif_value2[0], aif_value2[5], 0),
                rate_cal(aif_value2[1], aif_value2[6], 1),
                rate_cal(aif_value2[2], aif_value2[7], 0),
                rate_cal(aif_value2[3], aif_value2[8], 0),
            ];
            console.log('two', mitigate_rate_value_two)

            Highcharts.chart("ploar_chart1", {
                chart: {
                    polar: true,
                    type: "line",
                },
                title: {
                    text: "Protected Attribute : " + protect[0],
                    x: -30,
                },
                pane: {
                    size: "90%",
                },
                xAxis: {
                    categories: [
                        "Statistical Parity Difference",
                        "Disparate impact",
                        "Equal opportunity difference",
                        "Average odds difference",
                    ],
                    tickmarkPlacement: "on",
                    lineWidth: 0,
                },
                yAxis: {
                    gridLineInterpolation: "circle",
                    lineWidth: 0,
                    min: 0,
                },
                tooltip: {
                    shared: true,
                    pointFormat: "{point.y:,.0f}%",
                },
                legend: {
                    align: "right",
                    verticalAlign: "middle",
                },
                series: [
                    {
                        type: "area",
                        color: "rgba(255, 0, 0, 0)",
                        fillOpacity: 0.5,
                        data: mitigate_rate_value_one,
                        pointPlacement: "on",
                    },
                ],
                plotOptions: {
                    series: {
                        gapSize: 5,
                    },
                },
                responsive: {
                    rules: [
                        {
                            condition: {
                                maxWidth: 500,
                            },
                            chartOptions: {
                                legend: {
                                    enabled: false,
                                },
                            },
                        },
                    ],
                },
            });

            Highcharts.chart("ploar_chart2", {
                chart: {
                    polar: true,
                    type: "line",
                },
                title: {
                    text: "Protected Attribute : " + protect[2],
                    x: -30,
                },
                pane: {
                    size: "90%",
                },
                xAxis: {
                    categories: [
                        "Statistical Parity Difference",
                        "Disparate impact",
                        "Equal opportunity difference",
                        "Average odds difference",
                    ],
                    tickmarkPlacement: "on",
                    lineWidth: 0,
                },
                yAxis: {
                    gridLineInterpolation: "circle",
                    lineWidth: 0,
                    min: 0,
                },
                tooltip: {
                    shared: true,
                    pointFormat: "{point.y:,.0f}%",
                },
                legend: {
                    align: "right",
                    verticalAlign: "middle",
                },
                series: [
                    {
                        type: "area",
                        color: "rgba(18, 154, 144, 0)",
                        fillOpacity: 0.5,
                        data: mitigate_rate_value_two,
                        pointPlacement: "on",
                    },
                ],
                plotOptions: {
                    series: {
                        gapSize: 5,
                    },
                },
                responsive: {
                    rules: [
                        {
                            condition: {
                                maxWidth: 500,
                            },
                            chartOptions: {
                                legend: {
                                    enabled: false,
                                },
                            },
                        },
                    ],
                },
            });

            $("#ploar_chart1 .highcharts-legend").remove();
            $("#ploar_chart2 .highcharts-legend").remove();
            $("#ploar_chart1 .highcharts-exporting-group").remove();
            $("#ploar_chart2 .highcharts-exporting-group").remove();
            $("button").eq(2).remove();
            $("button").eq(3).remove();
            $("button").eq(4).remove();
            $("button").eq(5).remove();
            $("button").eq(6).remove();
            $("button").eq(7).remove();
        },
        error: function (request, status, error) {
            alert(error);
            console.group("err!!!");
            console.log(request)
            console.log(status)
            console.groupEnd();
        },
    });
}
