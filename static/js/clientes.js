function validar(form) {
    var password = form.password.value;
    var mensaje = validarLongitudPassword(password);
    mensaje += passwordRobusto(password);
    console.log(mensaje);
    var div = document.getElementById("notificaciones");
    var ban = false;

    if (mensaje != "") {
        div.innerHTML = mensaje;
        ban = false;
    }
    else {
        div.innerHTML = "";
        ban = true;
    }
    return ban;
}

function validarLongitudPassword(cadena) {
    var salida = "";
    if (cadena.length < 8) {
        salida = '¡El password tiene que tener 8 caracteres! <br>'
    }
    return salida;
}

function unDigito(cadena) {/*tenga un digito el password*/
    var ban = false;
    for (i = 0; i < cadena.length; i++) {
        var cod = cadena.charCodeAt(i);
        if (cod >= 48 && cod <= 57) {
            ban = true;
            break;
        }
    }
    return ban;
}
function passwordRobusto(cadena) {
    var salida = "";
    if (!unDigito(cadena)) {
        salida += 'El password tiene que  incluir un digito. <br>';
    }
    if (!tieneMayuscula(cadena)) {
        salida += 'La contraseña debe incluir al menos una letra en Mayuscula. <br>';
    }
    if (!tieneCaracerEspecial(cadena)) {
        salida += 'La contraseña debe incluir al menos un caracter especial. <br>';

    }
    return salida;
}

function tieneMayuscula(cadena) {/*tenga una mayuscula el password*/
    var ban = false;
    for (i = 0; i < cadena.length; i++) {
        var cod = cadena.charCodeAt(i);
        if ((cod >= 65 && cod <= 90) || cod == 165) {
            ban = true;
            break;
        }
    }
    return ban;
}

function tieneCaracerEspecial(cadena) {/*tenga un caracter especial el password*/
    var ban = false;
    for (i = 0; i < cadena.length; i++) {
        var cod = cadena.charCodeAt(i);
        if ((cod >= 32 && cod <= 47) || (cod >= 58 && cod <= 64) || (cod >= 91 && cod <= 96) || (cod >= 123 && cod <= 126) || cod == 168 || cod == 173 || cod == 239) {
            ban = true;
            break;
        }
    }
    return ban;
}


function consultarEmail() { 
    var ajax = new XMLHttpRequest();
    var email = document.getElementById("email");
    var url = "/usuarios/email/" + email.value;
    var div = document.getElementById("notificaciones");
    ajax.open("get", url, true);
    ajax.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
          var respuesta=JSON.parse(this.responseText);
          if(respuesta.estatus=="Error" ){
           email.value=null    
           div.innerHTML=respuesta.mensaje;
          }
          else{
            console.log(respuesta);  
            div.innerHTML="";
          }
        }
    };
    ajax.send();
}
