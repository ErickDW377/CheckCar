function calcularTotal(){
    var ajax=new XMLHttpRequest();
    var manoObra=document.getElementById("manoObra").value;
    var id=document.getElementById("id").value;
    manoObra = parseFloat(manoObra)
    var url="/servicios/detallesTotal/"+id;    
    var total=document.getElementById("total");   
       
    ajax.open("get",url,true);
    ajax.onreadystatechange=function(){
        if(this.readyState==4 && this.status==200){
            var respuesta=JSON.parse(this.responseText);
            if(respuesta.estatus=='OK'){      
                
                total.value= respuesta.suma+ manoObra;
                
                console.log(respuesta.suma);
            }
            
        }
    };
    ajax.send();
}