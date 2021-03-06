let socket = null;
let name = null;
let room = null;

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (~tab.url.indexOf('leetcode.com')) {
      chrome.pageAction.show(tabId);
    } else {
        chrome.pageAction.hide(tabId);
    }
});

chrome.runtime.onMessage.addListener((message) => {
    if (message.type == 'join') {
        room = message.data.room;
        name = message.data.name;

        join(room, name);
    } else if (message.type == 'leave') {
        leave();
    } else if (message.type == 'run') {
        run(message.data.problem);
    } else if (message.type == 'solution_accepted') {
        solution_accepted(message.data.problem, message.data.code);
    } else if (message.type == 'solution_declined') {
        solution_declined(message.data.problem);
    }

    console.log(name);
});

function join(room, name) {
    socket = io('https://litcode.herokuapp.com');
    // For testing: socket = io('http://localhost:5000');

    socket.on('connect', () => {
        socket.emit('join', {
            'room': room,
            'name': name
        });
    });

    socket.on('join_accepted', () => {
        chrome.runtime.sendMessage({'type': 'join_accepted'});
    });
}

function leave() {
    socket.close();
    socket = name = room = null;
}

function run(problem) {
    if (socket) {
        socket.emit('run', {'problem': problem});
    }
}

function solution_accepted(problem, code) {
    if (socket) {
        socket.emit('solution_accepted', {'problem': problem, 'code': code});
    }
}

function solution_declined(problem) {
    if (socket) {
        socket.emit('solution_declined', {'problem': problem});
    }
}

function isConnected() {
    return !!socket;
}

function getName() {
    return name;
}

function getRoom() {
    return room;
}