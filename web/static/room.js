let FADE_TIME = 500;
let MAX_ACTION_COUNT = 2;

let socket = null;
let room = null;
let players = [];
let actionCount = 0;
let problem = '';

$(document).ready(() => {
    room = $('#room').val();
    
    setupSocket();

    $('#next_problem_btn').click(() => {
        if (socket) {
            socket.emit('next_problem', {});
        }
    });
});

function setupSocket() {
    socket = io('http://localhost:5000');

    socket.on('connect', () => {
        socket.emit('join', {
            'room': room,
            'name': null
        });
    });

    socket.on('room_info', (data) => {
        if (data.problem) {
            problem = data.problem;
            $('#problem').text(problem);
        }

        if (data.players) {
            players = data.players;
            players.sort((a, b) => a.name.localeCompare(b.name));
            updatePlayers();
        }
    });

    socket.on('run', (data) => {
        let name = data.name;
        addAction(`${name} ran their code.`);
    });

    socket.on('solution_accepted', (data) => {
        let name = data.name;
        addAction(`${name} solved the question.`, 'success');
    });

    socket.on('solution_declined', (data) => {
        let name = data.name;
        addAction(`${name} submitted an incorrect solution.`, 'danger');
    });
}

function updatePlayers() {
    $('#players').empty();

    for (let p of players) {
        let icon = '';

        if (p.accepted) {
            icon = '<i class="fas fa-check" title="Solved question"></i>';
        }

        $('#players').append(`<li>${p.name}${icon}</li>`);
    }
}

function addAction(action, type = 'primary') {
    actionCount++;

    if (actionCount > MAX_ACTION_COUNT) {
        actionCount--;
        let firstAction = $('#actions').find('.action').first();

        $(firstAction).fadeOut(FADE_TIME, () => {
            $(firstAction).remove();
        });
    }

    let alertHtml = `<div class="action alert alert-${type}" style="display:none"><h5>${action}</h5><br></div>`;
    
    $('#actions').append(alertHtml);
    
    let lastAction = $(`#actions`).find('.action').last();
    $(lastAction).fadeIn();
}