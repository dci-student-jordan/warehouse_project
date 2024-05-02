//show or hide login

const loginShower = document.querySelector('#loginShower')
const loginForm = document.querySelector('#loginForm');
const vanish = document.querySelector('#vanishingInv')

let keepLogIn = false

function setStyles(displayLoginForm, displayVanish, height) {
    loginForm.style.display = displayLoginForm;
    vanish.style.display = displayVanish;
    
    // if (screen.width < 600) {
    //     loginShower.style.height = height;
    // }
}

loginShower.addEventListener('mouseover', () => {
    setStyles('block', 'none', '20%');
});

function hideLogin() {
    if (!keepLogIn) {
        setStyles('none', 'block', '20%');
    }
}

// function submitMessage() {
//     loginForm.submit();
//     hideLogin()
// }

loginShower.addEventListener('mouseout', hideLogin);


// Add the 'loaded' class to the body when the page is fully loaded
document.addEventListener('DOMContentLoaded', function () {
    document.body.classList.add('loaded');
});