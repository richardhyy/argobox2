const ProfileTypeDiagramDescription = {
    "core": {
        "data_series": [
            {
                "name": "Salinity (PSU)",
                "source": "cpressure",
            },
            {
                "name": "Temperature (℃)",
                "source": "ctemperature",
            },
        ]
    },
    "bbp": {
        "data_series": [
            {
                "name": "Backscattering (m^-1)",
                "source": "cbackunknown",
            },
            {
                "name": "Backscattering470 (m^-1)",
                "source": "cback470",
            },
            {
                "name": "Backscattering532 (m^-1)",
                "source": "cback532",
            },
            {
                "name": "Backscattering700 (m^-1)",
                "source": "cback700",
            },
        ]
    },
    "cdom": {
        "data_series": [
            {
                "name": "CDOM (ppb)",
                "source": "ccdom",
            },
        ]
    },
    "chla": {
        "data_series": [
            {
                "name": "Chlorophyll-a (mg/m^3)",
                "source": "cchla",
            },
        ]
    },
    "doxy": {
        "data_series": [
            {
                "name": "TEMP_DOXY (℃)",
                "source": "ctempdoxy",
            },
            {
                "name": "Dissolved Oxygen (micromole/kg)",
                "source": "cdoxygen",
            },
        ]
    },
    "irra": {
        "data_series": [
            {
                "name": "Down Irradiance412 (W/m^2/nm)",
                "source": "cdownirra412",
            },
            {
                "name": "Down Irradiance443 (W/m^2/nm)",
                "source": "cdownirra443",
            },
            {
                "name": "Down Irradiance490 (W/m^2/nm)",
                "source": "cdownirra490",
            },
            {
                "name": "PAR (microMoleQuanta/m^2/sec)",
                "source": "cpar",
            },
        ]
    },
    "nitr": {
        "data_series": [
            {
                "name": "Nitrate (micromole/kg)",
                "source": "cnitrate",
            },
        ]
    },
    "ph": {
        "data_series": [
            {
                "name": "PH in situ total",
                "source": "cph",
            },
        ]
    },
};

document.getElementById('search-tip').innerText += Object.keys(ProfileTypeDiagramDescription).join()

// MARK: - Data Loading

let taskManager = new TaskManager("loading-modal");

taskManager.newTask(() => loadRemoteGeoJson(
        "api/header/all/all/latest",
        (source) => colorizeArgoPoints(source, 1),
        () => taskManager.removeTask("load-latest-header")),
    "load-latest-header",
    "Loading latest Argo float locations");

taskManager.commit();


// Mark: - Map Related Functions

function httpGet(url, onSuccess, onError) {
    $.ajax({
        url: url,
        type: 'GET',
        success: data => onSuccess(data),
        error: error => onError(error)
    })
}

function loadRemoteGeoJson(url, painter, onComplete, removeOthers = false) {
    httpGet(url,
        function (data) {
            console.log(data);
            let promise = Cesium.GeoJsonDataSource.load(data);
            promise.then(function (dataSource) {
                if (removeOthers) {
                    viewer.dataSources.removeAll();
                }
                viewer.dataSources.add(dataSource);
                painter(dataSource);
                onComplete();
            });
        },
        function (error) {
            alert(`Error occurred during requesting API`);
            console.log(error);
        })
}

function colorizeArgoPoints(dataSource, zIndex, color = "#2ca2a7", labeled = false) {
    taskManager.newTask(() => {
            let features = dataSource.entities.values;
            for (let i = 0; i < features.length; i++) {
                let argo = features[i];
                argo.billboard = undefined;
                argo.point = new Cesium.PointGraphics({
                    color: new Cesium.Color.fromCssColorString(color),
                    pixelSize: 14,
                    scaleByDistance: new Cesium.NearFarScalar(0, 1.0, 2.0e7, 0.5),
                    zIndex: zIndex,
                });
                argo.name = argo.id;
                if (labeled) {
                    argo.label = {
                        text: '' + argo.properties['cycle_number'].getValue(),
                        font: '12pt sans-serif',
                        style: Cesium.LabelStyle.FILL_AND_OUTLINE,
                        outlineWidth: 2,
                        verticalOrigin: Cesium.VerticalOrigin.BOTTOM,
                        pixelOffset: new Cesium.Cartesian2(0, -9)
                    }
                }
            }
            // make argo features globally available
            document.argoFeatures = features;

            taskManager.removeTask("colorize-argo-points");
        },
        "colorize-argo-points",
        "Colorizing Argo points");
    taskManager.commit();
}


// MARK: - Profile related
function loadProfile(platformNumber, cycleNumber, type = "core") {
    httpGet(`api/profile/${type}/${platformNumber}/${cycleNumber}`,
        function (data) {
            document.getElementById("profile-container").style.display = "block";

            let noDataLabel = document.getElementById("no-data-label");
            let diagram = document.getElementById("diagram-container");
            noDataLabel.style.display = "none";
            diagram.style.display = "none";

            let profile = data;
            if (profile.features.length === 0) {
                noDataLabel.style.display = "block";
            } else {
                diagram.style.display = "block";
                showProfileDiagram(profile.features[0].properties["cpressure"],
                    profile.features[0],
                    ProfileTypeDiagramDescription[type]);
            }
        },
        function (error) {
            alert(`Error: ${error.message}`);
        });
}

function showProfileDiagram(pressure, feature, diagramDescription) {
    let profileDom = document.getElementById("diagram-container");
    let profileChart = echarts.init(profileDom, 'dark');

    let colors = ['#6d82c4', '#e88181'];

    let legends = [];
    let series = [];
    diagramDescription['data_series'].forEach(element => {
        console.log(element);
        series.push({
            name: element['name'],
            type: 'line',
            smooth: true,
            emphasis: {
                focus: 'series'
            },
            label: {
                formatter: function (params) {
                    return params.value;
                }
            },
            data: feature.properties[element['source']]
        });
        legends.push(element['name']);
    });

    let option = {
        color: colors,
        backgroundColor: 'transparent',

        tooltip: {
            trigger: 'none',
            axisPointer: {
                type: 'cross'
            }
        },
        legend: {
            data: legends
        },
        grid: {
            top: 70,
            bottom: 50
        },
        xAxis: [
            {
                type: 'category',
                axisTick: {
                    alignWithLabel: true
                },
                axisLine: {
                    onZero: false,
                    lineStyle: {
                        color: colors[1]
                    }
                },
                axisPointer: {
                    label: {
                        formatter: function (params) {
                            return 'Pressure  ' + params.value + ' (dbar)';
                        }
                    }
                },
                data: pressure
            }
        ],
        yAxis: [
            {
                type: 'value'
            }
        ],
        series: series,
    };

    option && profileChart.setOption(option);

    profileChart.on('legendselectchanged', function (params) {
        selectGraph(params);
        unselectGrap(params);
    });

    function selectGraph(params) {
        profileChart.dispatchAction({
            type: 'legendSelect',
            name: params.name,
        })
    }

    function unselectGrap(params) {
        for (const legend in params.selected) {
            if(legend !== params.name) {
                profileChart.dispatchAction({
                    type: 'legendUnSelect',
                    // legend name
                    name: legend,
                })
            }
        }
    }
}


// MARK: - Util

Array.prototype.insert = function (index, item) {
    this.splice(index, 0, item);
};

function matchFloatList(keyword) {
    if (keyword === "") {
        return [];
    }
    let floats = document.argoFeatures;
    let result = [];
    for (let i = 0; i < floats.length; i++) {
        let float = floats[i];
        let platformNumber = float.properties["platform_number"].getValue();
        let projectName = float.properties["project_name"].getValue();
        if (platformNumber !== null) {
            let appearAt = platformNumber.toString().indexOf(keyword.toLowerCase());
            if (appearAt === -1 && projectName !== null) {
                appearAt = projectName.indexOf(keyword)
            }

            if (appearAt !== -1) {
                if (appearAt === 0) {
                    result.insert(0, platformNumber + " - " + projectName);
                } else {
                    result.push(platformNumber + " - " + projectName);
                }
            }
        }

        if (result.length > 9) { // avoid too many results (significantly slowing down the browser)
            break;
        }
    }
    return result;
}
