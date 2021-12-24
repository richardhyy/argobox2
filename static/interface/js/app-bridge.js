let bridge = undefined;

function setBridge(appBridge) {
    console.log('Bridge set');
    bridge = appBridge;
}

function sendBridgeMessage(value, type) {
    if (bridge) {
        let wrapper = {
            'type': type,
            'data': value
        }
        window['send' + bridge + 'ObjectMessage'](JSON.stringify(wrapper));
    }
}

let currentPoint = undefined;

function bridgeSetCurrentLocation(lon, lat) {
    if (currentPoint) {
        currentPoint.setLatLng([lat, lon]);
    } else {
        currentPoint = GeometriesHelper.createPoint(viewer, "Your Position", "",
            Cesium.Cartesian3.fromDegrees(lon, lat, 100),
            30,
            new Cesium.NearFarScalar(0, 1.0, 2.0e7, 0.5),
            undefined,
            new Cesium.DistanceDisplayCondition(0, 1000000),
            Cesium.HeightReference.NONE,
            Cesium.Color.ORANGE,
            true,
            Cesium.Color.SANDYBROWN,
            2);
    }
    viewer.zoomTo(currentPoint);
}

function hideSearchBar() {
    $('#searchbar').fadeOut();
}