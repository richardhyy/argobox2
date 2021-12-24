let bridge = undefined;

function setBridge(appBridge) {
    console.log('Bridge set');
    bridge = appBridge;
}

function sendBridgeMessage(value, type) {
    if (bridge) {
        let wrapper = {
            'type': type, 'data': value
        }
        window['send' + bridge + 'ObjectMessage'](JSON.stringify(wrapper));
    }
}

let currentPoint = undefined;

function bridgeSetCurrentLocation(lon, lat) {
    if (currentPoint) {
        currentPoint.setLatLng([lat, lon]);
    } else {
        currentPoint = viewer.entities.add({
            position: Cesium.Cartesian3.fromDegrees(lon, lat), billboard: {
                image: 'static/interface/images/marker.png', width: 24, height: 24
            }, label: {
                text: 'Your Position',
                font: '14pt monospace',
                style: Cesium.LabelStyle.FILL_AND_OUTLINE,
                outlineWidth: 2,
                verticalOrigin: Cesium.VerticalOrigin.TOP,
                pixelOffset: new Cesium.Cartesian2(0, 32)
            }
        });
    }
    viewer.zoomTo(currentPoint);
}

function hideSearchBar() {
    $('#searchbar').fadeOut();
}