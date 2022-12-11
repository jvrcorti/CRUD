
const nombre = document.getElementById("name");
const email = document.getElementById("email");
const consulta = document.getElementById("consulta");
const form = document.getElementById("form");
const parrafo = document.getElementById("warnings");
const $buttonmailto = document.querySelector('tomail');

form.addEventListener("submit", e=>{
    e.preventDefault()
    let warnings = ""
    let entrar = false
    let regexname = /^[a-zA-Z]+$/
    let regexEmail = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,4})+$/
    parrafo.innerHTML = ""
    if(!regexname.test(nombre.value)){
        if(nombre.value.length === 0){
            warnings += 'Debe ingresar su nombre y apellido <br>'
            entrar = true
        }else if(nombre.value.length >= 30){
            warnings += 'Su nombre y apellido debe ser menor <br>'
            entrar = true
        }   
        else {warnings += `El nombre no es valido. <br>`
        entrar = true
        }
    }
    if(!regexEmail.test(email.value)){
        warnings += `El email no es valido. <br>`
        entrar = true
    }
    if(consulta.value.length === 0){
        warnings += `No ingresaste tu consulta. <br>`
        entrar = true
    }
    if(entrar){
        parrafo.innerHTML = warnings
    }else{
        parrafo.innerHTML = "Enviado"
    }
})

