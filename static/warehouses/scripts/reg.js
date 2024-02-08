// Function to load the update user data form
function loadUserForm(form) {  
    fetch(form)
        // Use AJAX to fetch the HTML content for the update user data form
        // and inject it into the dynamicContent div
        .then(response => response.text())
        .then(data => {
            document.getElementById('dynamicContent').innerHTML = data;
            // hack for mouseout
            const keep_alives = document.querySelectorAll('.keep_alive')
            keep_alives.forEach(element => {
                handleFocusAndBlur(element)
                console.log("keep_alive for", element.id)
            });
            // needs reload
            if (form.endsWith('logout')) {
                location.reload()
            }
            // When submitting we want to return to the current page
            var currentPageUrl = window.location.href;    
            // Construct the URL with "?next=" plus the current page URL
            var nextUrl = '?next=' + encodeURIComponent(currentPageUrl);    
            // Get the form element
            var new_form = document.querySelector('#new-form');
            // Append the nextUrl to the form's action attribute
            new_form.action += nextUrl;
        });
    if (form.endsWith('signup') | form.endsWith('login')) {
        var hide = form.endsWith('signup') ? 'signup' : 'login';
        var show = form.endsWith('login') ? 'signup' : 'login';
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