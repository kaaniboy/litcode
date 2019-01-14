let POLL_INTERVAL = 10000;
let pollHandle;

let usernames = [];

$(document).ready(() => {
    $('#setup_modal').modal('show');

    $('#start_btn').click((e) => {
        e.preventDefault();
        startSession(); 
    });
});

function startSession() {
    $('#start_box').hide();

    usernames = $('#usernames').tagsinput('items');
    console.log(usernames);

    pollHandle = setInterval(() => {
        for (let u of usernames) {
            check(u, 'Minimum Distance Between BST Nodes');
        }
    }, POLL_INTERVAL);
}

function stopSession() {
    clearInterval(pollHandle);
}

function check(username, question) {
    $.ajax({
        type: "POST",
        url: '/check',
        data: {
            username: username,
            question: question
        },
        success: (solved) => {
            if (solved === "True") {
                console.log(username + ' has solved ' + question);
                stopSession();
            }
        }
    });
}