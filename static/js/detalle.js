unidades = 0;

function productoSeleccionado(){
    var ajax=new XMLHttpRequest();
    var producto=document.getElementById("producto").value;    
    var url="/producto/precio/"+producto;
    var cantidad=document.getElementById("cantidad");
    var costo=document.getElementById("costo"); 
    var total=document.getElementById("total"); 
    cantidad.value = 1;
       
    ajax.open("get",url,true);
    ajax.onreadystatechange=function(){
        if(this.readyState==4 && this.status==200){
            var respuesta=JSON.parse(this.responseText);
            if(respuesta.estatus=='OK'){
                //costo.innerHTML=respuesta.precio;
                costo.value=respuesta.precio;
                total.value= respuesta.precio*1;
                unidades = respuesta.cantidad;
                console.log(unidades);
            }
            else{
                costo.value=null;
                console.log(respuesta.precio);
            }
        }
    };
    ajax.send();
}

function calcularTotal(){
    var cantidad=document.getElementById("cantidad");
    var costo=document.getElementById("costo").value;
    var total=document.getElementById("total");    
    if(validarUnidader(cantidad.value)){
        total.value = cantidad.value*costo;
    }else{
        alert("Unidades insuficientes actualmente cuentas solo con " + unidades + " unidades disponibles");
        cantidad.value = unidades;
    }
    
}

function validarUnidader(cantidad){
    console.log(unidades);
    if (cantidad<= unidades){
        return true;
    }else{
        return false;
    }
}