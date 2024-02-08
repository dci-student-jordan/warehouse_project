// Function to load the update user data form
function loadUserForm(form) {
    // Use AJAX to fetch the HTML content for the update user data form
    // and inject it into the dynamicContent div
    fetch(form)
        .then(response => response.text())  // assuming the server returns JSON
        .then(data => {
            document.getElementById('dynamicContent').innerHTML = data;
            const keep_alives = document.querySelectorAll('.keep_alive')
            keep_alives.forEach(element => {
                handleFocusAndBlur(element)
                console.log("keep_alive for", element.id)
            });
        });
    if (form.endsWith('signup') | form.endsWith('login/')) {
        var hide = form.endsWith('signup') ? 'signup' : 'login';
        var show = form.endsWith('login/') ? 'signup' : 'login';
        hide_btn = document.getElementById(hide)
        show_btn = document.getElementById(show)
        hide_btn.style.display = 'none';
        show_btn.style.display = 'block';
    }
}

function handleFocusAndBlur(element) {
    if (element) {
        element.addEventListener('focus', () => keepLogIn = true);
        element.addEventListener('blur', () => {
            keepLogIn = false;
        });
    }
}