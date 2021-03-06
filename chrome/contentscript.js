let POLL_INTERVAL = 500;
let ACCEPTED_TEXT = 'Submission Result: Accepted';
let DECLINED_TEXT = 'Submission Result: Wrong Answer';
let COMPILE_ERROR_TEXT = 'Submission Result: Compile Error';
let TIMELIMIT_EXCEEDED_TEXT = 'Submission Result: Time Limit Exceeded'
let problem = null;
let runButton = null;
let submitButton = null;

$(document).ready(() => {
    setup();
});

function setup() {
    runButton = $($('.action .row .pull-right')[1]).find('button')[0];
    submitButton = $($('.action .row .pull-right')[1]).find('button')[1];
    problem = $('h3').text();

    // Keep trying until both buttons are present
    if (!runButton || !submitButton) {
        setTimeout(setup, 500);
    } else {
        $(runButton).click(runCode);
        $(submitButton).click(submitCode);
        console.log('Litcode initialized.')
    }
}

function runCode() {
    chrome.runtime.sendMessage({
        'type': 'run',
        'data': {
            'problem': problem
        }
    });
    console.log('Run code.');
}

function submitCode() {
    let code = $('[name="lc-codemirror"]').text();

    let id = setInterval(() => {
        console.log('POLLING!');
        let resultText = $('#result').text();

        if (~resultText.indexOf(ACCEPTED_TEXT)) {
            console.log('POLLING DONE: ACCEPTED');
            clearInterval(id);
            chrome.runtime.sendMessage({
                'type': 'solution_accepted',
                'data': {
                    'problem': problem,
                    'code': code
                }
            });
        } else if (~resultText.indexOf(DECLINED_TEXT) 
                    || ~resultText.indexOf(COMPILE_ERROR_TEXT)
                    || ~resultText.indexOf(TIMELIMIT_EXCEEDED_TEXT)) {
            console.log('POLLING DONE: DECLINED');
            clearInterval(id);
            chrome.runtime.sendMessage({
                'type': 'solution_declined',
                'data': {
                    'problem': problem
                }
            });
        }
    }, POLL_INTERVAL);
}