function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if the cookie name matches the requested name
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function hack_mouseover() {
    // hack for mouseout
    const keep_alives = document.querySelectorAll('.keep_alive')
    keep_alives.forEach(element => {
        handleFocusAndBlur(element)
    });
}

// Function to load the update user data form
function loadUserForm(form) {  
    fetch(form)
        // Use AJAX to fetch the HTML content for the update user data form
        // and inject it into the dynamicContent div
        .then(response => response.text())
        .then(data => {
            // needs reload
            if (form.endsWith('logout/')) {
                location.reload()
            }
            else {
                document.getElementById('dynamicContent').innerHTML = data;
                hack_mouseover()
                prepareNewForm(form)
            }
        });
    if (form.endsWith('signup/') | form.endsWith('login/')) {
        var hide = form.endsWith('signup/') ? 'signup' : 'login';
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

function prepareNewForm (form_string) {
    if (form_string.endsWith('login')) {
        new_form = document.getElementById('new-form')
        action = new_form.action
        new_form.action= action + "?next=" + window.location.href;
    }
    document.getElementById('new-form').addEventListener('submit', function(event) {
        event.preventDefault();
        let form = event.target;
        let formData = new FormData(form);
        
        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data["html"] == "") location.reload();
            else {
            // Replace #dynamiccontent with the fetched content
            document.querySelector('#dynamicContent').innerHTML = data["html"];
            var errors = document.querySelectorAll('[class^="errorlist"]');
            for (var i = 0; i < errors.length; i++) {
                // Apply the red color style to each error element
                errors[i].style.color = 'red';
            }
            hack_mouseover()}
            prepareNewForm(form_string)
        })
        .catch(error => {
            console.error('Error:', error);
            // Handle errors if needed
        });
    });}