class MainComponent {
    constructor({splineContainerId, barContainerId, projectId, maskContainerId, progressId}) {
        this.splineContainerId = splineContainerId;
        this.barContainerId = barContainerId;
        this.maskContainer = document.getElementById(maskContainerId);
        this.progress = document.getElementById(progressId);

        this.initProject(projectId);
        this.title = document.getElementsByTagName('title')[0];
    }

    initProject(projectId) {
        Request.get(`https://data.6-79.cn/v1/project/@${projectId}`)
            .then(data => {
                this.project = new Project(data);
                this.title.innerText = '数据食堂 - ' + this.project.name;
                this.crazyFetch = new CrazyFetch(this.project);
                this.crazyFetch.fetchNewData(this.progress)
                    .then(this.prepareData.bind(this));
            });
    }

    prepareData(dataFlow) {
        this.maskContainer.remove();
        // dataFlow = dataFlow.slice(dataFlow.length - 10);
        // dataFlow = dataFlow.slice(1);
        this.splineSeries = [];
        this.barSeries = [{
            name: '',
            data: [],
            dataSorting: {
                enabled: true,
                sortKey: 'y',
            },
        }];
        this.labels = [];
        dataFlow.forEach(data => {
            let time = data.time * 1000;
            data.waves.forEach(wave => {
                let index = this.labels.indexOf(wave.label);
                if (index === -1) {
                    this.splineSeries.push({name: wave.label, data: []});
                    this.labels.push(wave.label);
                    index = this.labels.indexOf(wave.label);
                }
                this.splineSeries[index].data.push({x: time, y: wave.value});
                this.barSeries[0].data[index] = [wave.label, wave.value];
            });
        });

        this.splineTitle = this.project.name + '时间折线图';
        this.barTitle = this.project.name + '实时柱形图';
        this.initSplineGraph();
        this.initBarGraph();
        this.updateData();
    }

    updateData() {
        setInterval( () => {
            this.crazyFetch.fetchNewData()
                .then((dataFlow) => {
                    if (!dataFlow.length) {
                        return;
                    }
                    dataFlow.forEach(data => {
                        let time = data.time * 1000;
                        let barData = [];
                        data.waves.forEach(wave => {
                            let index = this.labels.indexOf(wave.label);
                            if (index === -1) {
                                this.splineChart.addSeries({name: wave.label, data: []});
                                this.labels.push(wave.label);
                                index = this.labels.indexOf(wave.label);
                            }
                            this.splineChart.series[index].addPoint([time, wave.value], true, false);
                            barData[index] = wave.value;
                        });
                        this.barChart.series[0].setData(barData);
                    })
                })
        }, 5000);
    }

    initBarGraph() {
        this.barChart = Highcharts.chart(this.barContainerId, {
            chart: {
                type: 'bar',
                animation: Highcharts.svg, // don't animate in old IE
                marginRight: 10,
                zoomType: 'xy',
            },
            title: {
                text: this.barTitle,
            },
            xAxis: {
                type: 'category',
                labels: {
                    animate: true,
                },
                title: {
                    text: null
                }
            },
            yAxis: {
                min: 0,
                title: {
                    text: '',
                    align: 'high'
                },
                labels: {
                    overflow: 'justify'
                }
            },
            tooltip: {
            },
            plotOptions: {
                bar: {
                    dataLabels: {
                        enabled: true,
                        overflow: "justify"
                    }
                },
            },
            legend: {
                enabled: false,
            },
            credits: {
                enabled: false
            },
            series: this.barSeries,
        });
    }

    initSplineGraph() {
        this.splineChart = Highcharts.chart(this.splineContainerId, {
            chart: {
                type: 'spline',
                animation: Highcharts.svg, // don't animate in old IE
                marginRight: 10,
                zoomType: 'xy',
            },
            colors: [
                '#7cb5ec', '#434348', '#90ed7d', '#f7a35c',
                '#8085e9', '#f15c80', '#e4d354', '#8d4653',
                '#91e8e1', '#3139CB', '#19781E', '#782519'],
            plotOptions: {
                series: {
                    turboThreshold: 0,
                    lineWidth: 4,
                },
                turboThreshold: 10,
            },
            time: {
                useUTC: false
            },
            title: {
                text: this.splineTitle,
            },
            xAxis: {
                type: 'datetime',
                tickPixelInterval: 150,
            },
            yAxis: {
                title: {
                    text: ''
                },
            },
            tooltip: {
                headerFormat: '<b>{series.name}</b><br/>',
                pointFormat: '{point.x:%Y-%m-%d %H:%M:%S}<br/>{point.y}'
            },
            exporting: {
                enabled: true,
                filename: this.splineTitle,
            },
            series: this.splineSeries,
            credits: {
                enabled: false
            },
        });
    }
}