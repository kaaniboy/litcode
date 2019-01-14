let bg = chrome.extension.getBackgroundPage();

$(document).ready(() => {
    setupMessageListeners();

    if (bg.isConnected()) {
        setupConnectedView();
    } else {
        setupJoinView();
    }

    $('#join_btn').click(() => join($('#room').val(), $('#name').val()));
    $('#leave_btn').click(() => leave());
});

function setupConnectedView() {
    $('#connected_view').show();
    $('#join_view').hide();

    $('#connected_text').html(`Connected as <b>${bg.getName()}</b> to room <b>${bg.getRoom()}</b>`);
}

function setupJoinView() {
    $('#connected_view').hide();
    $('#join_view').show();
}

function setupMessageListeners() {
    chrome.runtime.onMessage.addListener((message) => {
        if (message.type == 'join_accepted') {
            setupConnectedView();
        }
    });
}

function join(room, name) {
    chrome.runtime.sendMessage({
        'type': 'join',
        'data': {
            'room': room,
            'name': name
        }
    });
}

function leave() {
    chrome.runtime.sendMessage({'type': 'leave'});
    setupJoinView();
}