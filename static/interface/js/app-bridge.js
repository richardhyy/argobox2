let bridge = undefined;

function setBridge(appBridge) {
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

function bridgeSetCurrentLocation(lon, lat){
    let currentPoint = GeometriesHelper.createPoint(viewer, "Your Position", "",
        Cesium.Cartesian3.fromDegrees(lon, lat, 300000.0),
        30,
        new Cesium.NearFarScalar(100, 1, 2000000, 10),
        new Cesium.NearFarScalar(100, 1, 2000000, 0.5),
        new Cesium.DistanceDisplayCondition(0, 1000000),
        Cesium.HeightReference.NONE,
        Cesium.Color.AQUA,
        true,
        Cesium.Color.ROSYBROWN,
        2);
    viewer.zoomTo(currentPoint);
}
