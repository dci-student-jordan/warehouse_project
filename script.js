//show or hide login

const loginShower = document.querySelector('#loginShower')
const loginForm = document.getElementById('loginForm')
const vanish = document.querySelector('#vanishingInv')

loginShower.addEventListener('mouseover', () => {
    loginForm.style.display = 'block'
    vanish.style.display = 'none';
    if (screen.width < 600)
        loginShower.style.height = '300px';
})


function hideLogin() {
    loginForm.style.display = 'none'
    vanish.style.display = 'block';
    if (screen.width < 600)
        loginShower.style.height = '20%';
}

loginShower.addEventListener('mouseout', () => hideLogin())


// loginForm functionality

function isValidMessage () {
    var em = document.querySelector('#email').value
    var isEmail = /^\S+@\S+\.\S+$/.test(em)
    submitter = document.querySelector('#submitMess')
    if (isEmail &
        (document.querySelector('#message').value != "") &
        (document.querySelector('#name').value != "")) {
            submitter.textContent = "submit";
            console.log("submittable");
    }
    else submitter.textContent = "cancel";
}

function sendMess () {
    button = document.querySelector('#submitMess');
    if (button.textContent == "submit") {
        window.location.href = "mailto:aware_shopping@world.earth"+"?subject=nicely submitted Mail by "+document.querySelector('#name').value+"&body="+document.querySelector('#message').value+"%0D%0A%0D%0AAnswer: "+document.querySelector('#email').value
    }
    else hideLogin()
}
