let bridge = undefined;

function sendBridgeMessage(value, type) {
    if (bridge) {
        let wrapper = {
            'type': type,
            'data': value
        }
        window['send' + bridge + 'ObjectMessage'](JSON.stringify(wrapper));
    }
}

