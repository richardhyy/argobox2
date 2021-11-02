let selectedEntity;
let defaultDiagramType = "core";

function search() {
    let searchWord = $('#search-text').val();
    if (searchWord === "") {
        searchWord = "3900515 chla";
        $('#search-text').val(searchWord);
    }

    let profileType = "all";
    let platformNumber = "all";
    if (searchWord.includes(" ")) {
        split = searchWord.split(" ");
        split.forEach(part => {
            hit = false;
            if (ProfileTypeDiagramDescription.hasOwnProperty(part)) {
                profileType = part;
                hit = true;
            }
            if (!hit && !isNaN(part)) {
                platformNumber = parseInt(part);
            }
        })
    } else {
        if (!isNaN(searchWord)) {
            platformNumber = parseInt(searchWord);
        } else if (ProfileTypeDiagramDescription.hasOwnProperty(searchWord)) {
            profileType = searchWord;
        }
    }

    if (profileType !== "all") {
        defaultDiagramType = profileType;
    } else {
        defaultDiagramType = "core";
    }

    let taskManager = new TaskManager("loading-modal");

    if (platformNumber === "all") {
        taskManager.newTask(() => loadRemoteGeoJson(
            `api/header/${profileType}/all/latest`,
            (source) => colorizeArgoPoints(source, 1),
            () => taskManager.removeTask("load-latest-header"),
            true),
        "load-latest-header",
        "Loading latest Argo float locations");
    } else {
        let geoserverUrl = `api/header/${profileType}/${platformNumber}/all`;

        taskManager.newTask(() => $.ajax({
                url: geoserverUrl,
                type: 'GET',
                success: function (data) {
                    // Hide search completion view
                    document.getElementById("search-completion").style.display = "none";

                    console.log(data);
                    let features = data;
                    if (features.totalFeatures >= 1) {
                        // add to layer
                        let promise = Cesium.GeoJsonDataSource.load(features);
                        promise.then(function (dataSource) {
                            viewer.dataSources.add(dataSource);
                            colorizeArgoPoints(dataSource, 1, "#6de398", true);
                        });

                        // locate to target
                        // let lonlat = features.features[0].geometry.coordinates;
                        // console.log(lonlat, lonlat[0], lonlat[1]);
                        // camera.flyTo({destination: Cesium.Cartesian3.fromDegrees(lonlat[0], lonlat[1], 55000)});

                        let coordinateList = []
                        for (let x of features.features) {
                            coordinateList.push(x.geometry.coordinates[0]);
                            coordinateList.push(x.geometry.coordinates[1]);
                        }

                        viewer.zoomTo(GeometriesHelper.createPolyline(viewer,
                            `Trace ${searchWord}`,
                            Cesium.Cartesian3.fromDegreesArray(coordinateList),
                            8,
                            new Cesium.PolylineGlowMaterialProperty({
                                glowPower: 0.2,
                                taperPower: 0.5,
                                color: Cesium.Color.CORNFLOWERBLUE,
                            })
                        ));
                    }

                    taskManager.removeTask("search-float");
                },
                error: function (error) {
                    taskManager.removeTask("search-float");
                    console.log(error);
                }
            }),
            "search-float",
            `Searching for ${searchWord}`
        );
    }

    taskManager.commit();
}

function searchCompletion() {
    let list = matchFloatList($('#search-text').val());
    let target = document.getElementById("search-completion-list");
    if (list.length === 0) {
        document.getElementById("search-completion").style.display = "none";
        return;
    }

    document.getElementById("search-completion").style.display = "block";
    target.innerHTML = "";
    list.forEach(item => {
        let targetText = item.indexOf(" - ")===-1 ? item : item.split(" - ")[0];
        target.innerHTML += `<li onclick="$('#search-text').val('${targetText}')">${item}</li>`;
    })
}

function loadProfileForSelected(type) {
    console.log(selectedEntity);
    if (Cesium.defined(selectedEntity)) {
        if (Cesium.defined(selectedEntity.name)) {
            console.log('Selected ' + selectedEntity.name);
            if (selectedEntity.properties !== undefined) {
                let platformNumber = selectedEntity.properties["platform_number"];
                let cycleNumber = selectedEntity.properties["cycle_number"];
                loadProfile(platformNumber, cycleNumber, type);
                return;
            }
            console.log("Closing diagram.");
        } else {
            console.log('Unknown entity selected.');
        }
    } else {
        console.log('Deselected.');
    }
    clearProfileList();

}

function clearProfileList() {
    document.getElementById("profile-container").style.display = "none";
}

$('#search-text').focus();
$('#search-text').keypress(function (e) {
    const key = e.which;
    if(key === 13)  // the enter key code
    {
        search();
        return false;
    } else { // Match lake
    }
});
$('#search-text').on('input', function () {
    searchCompletion();
});

$('#search-btn').on('click', search);

$('#bottom-notification').on('click', function () {
    $('#bottom-notification').fadeOut();
})

viewer.selectedEntityChanged.addEventListener(function(entity) {
    selectedEntity = entity;
    console.log(selectedEntity);
    loadProfileForSelected(defaultDiagramType);
});