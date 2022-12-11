var userPassword = document.getElementById('user-password')
var userEmail = document.getElementById('user-email')
var changeButton = document.getElementById('show-password')
var passwordState = 0;
var alertDismiss = document.getElementById('alert-dismiss')
var mismatchAlert = document.getElementById('mismatch-alert')


changeButton.onclick = ()=> {
    if (passwordState==0){
        userPassword.type = 'text';
        passwordState = 1;
    }
    else if(passwordState==1){
        userPassword.type = 'password';
        passwordState = 0;
    }
}

alertDismiss.onclick = ()=> {
    mismatchAlert.style.display = 'none'
}