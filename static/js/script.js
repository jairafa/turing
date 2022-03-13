/*Inicio funciones index*/
/*Inicio funcion abrir menu lateral derecho info gestor*/
$(".abrir").click(function() {
    if ($(window).width() > 600) {
        //$(".cerrar").show();
        if ($("#sidebar").width() > 1) {
            $("#sidebar").animate({
                width: "0em",
                padding: "0em"
            }, 50, function() {});
            $(".cerrar").hide();
        } else {
            $("#sidebar").animate({
                width: "25em",
                padding: "0.5em 2em"
            }, 50, function() {});
            $(".cerrar").show();
        }
    } else {
        if ($("#sidebar").width() > 1) {
            $("#sidebar").animate({
                width: "0em",
                padding: "0em"
            }, 50, function() {});
            $(".cerrar").hide();
        } else {
            $("#sidebar").animate({
                width: "100%",
                padding: "0.5em 2em"
            }, 50, function() {});
            $(".cerrar").show();
        }
    }
});
$(".cerrar").click(function() {
    $("#sidebar").animate({
        width: "0%",
        padding: "0em"
    }, 50, function() {});
    $(".cerrar").hide();
});
/*Fin funcion abrir menu lateral derecho info gestor*/
/*Inicio funcion cerrar menu lateral derecho info gestor*/
$(document).on("click", function(e) {
    var container = $("#sidebar");
    var container2 = $(".abrir");
    var container3 = $(".container_busca_p_id");
    var container4 = $("#busca_p_id");
    var container5 = $("#button_submenu");
    var container6 = $("#menu");
    if (!container3.is(e.target) && container3.has(e.target).length === 0 && !container4.is(e.target) && container4.has(e.target).length === 0) {
        $('.container_busca_p_id').slideUp();
    }
    if (!container5.is(e.target) && container5.has(e.target).length === 0 && !container6.is(e.target) && container6.has(e.target).length === 0) {
         $('#menu').slideUp();
    }
    if (!container.is(e.target) && container.has(e.target).length === 0 && !container2.is(e.target) && container2.has(e.target).length === 0) {
        // alert("¡Pulsaste fuera!");
        $("#sidebar").animate({
            width: "0em",
            padding: "0em"
        }, 50, function() {});
        $(".cerrar").hide();
    }
});
/*Fin funcion cerrar menu lateral derecho info gestor*/
/*Inicio funcion cerrar menu lateral derecho info gestor onclick contenido*/
$("#princ").click(function() {
    $("#sidebar").animate({
        width: "0em",
        padding: "0"
    }, 5, function() {
        setTimeout(function() {
            $(".cerrar").hide();
        }, 300);
    });
});
/*Fin funcion cerrar menu lateral derecho info gestor*/
$(".home").click(function() {
    $(".contenido_principal").hide();
    $(".gif_cargando").show();
});



$(function () {
  $('[data-toggle="tooltip"]').tooltip()
});
/*Inicio Funcion detectar inactividad*/
/**
 *  JQuery Idle.
 *  A dead simple jQuery plugin that executes a callback function if the user is idle.
 *  Autor:Juan :v
 *  Juan David Rodriguez (judaropid1@gmail.com).
 *  About: Version
 *  1.2.6
 **/
! function(n) {
    "use strict";
    n.fn.idle = function(e) {
        var t, i, o = {
                idle: 6e4,
                events: "mousemove keydown mousedown touchstart",
                onIdle: function() {},
                onActive: function() {},
                onHide: function() {},
                onShow: function() {},
                keepTracking: !0,
                startAtIdle: !1,
                recurIdleCall: !1
            },
            c = e.startAtIdle || !1,
            d = !e.startAtIdle || !0,
            l = n.extend({}, o, e),
            u = null;
        return n(this).on("idle:stop", {}, function() {
            n(this).off(l.events), l.keepTracking = !1, t(u, l)
        }), t = function(n, e) {
            return c && (e.onActive.call(), c = !1), clearTimeout(n), e.keepTracking ? i(e) : void 0
        }, i = function(n) {
            var e, t = n.recurIdleCall ? setInterval : setTimeout;
            return e = t(function() {
                c = !0, n.onIdle.call()
            }, n.idle)
        }, this.each(function() {
            u = i(l), n(this).on(l.events, function() {
                u = t(u, l)
            }), (l.onShow || l.onHide) && n(document).on("visibilitychange webkitvisibilitychange mozvisibilitychange msvisibilitychange", function() {
                document.hidden || document.webkitHidden || document.mozHidden || document.msHidden ? d && (d = !1, l.onHide.call()) : d || (d = !0, l.onShow.call())
            })
        })
    }
}(jQuery);
$(document).idle({
    onIdle: function() {
        //location.replace("{% url 'logout' %}");
        //location.replace("logout/");

        //alert("se cerro la sesion");
    },
    idle: 1200000 //Tiempo maximo de inactividad
})
/*Fin funcion detectar inactividad*/
/*Inicio de funcion para que cada vez que cargue un iframe calcule el ancho*/
$(document).ready(function() {
    $('.contenido_principal').show();
    $(".gif_cargando").hide();
    $("body").animate({
        scrollTop: 0
    }, 500);
});
/*Fin de funcion para que cada vez que cargue un iframe calcule el ancho*/
/*Inicio funcion para mostrar hoja de vida*/
function hv(ruta, contenedor, identificador) {
    window.parent.$("iframe").animate({
        scrollTop: 0
    }, 500);
    window.parent.$(".gif_cargando").show();
    window.parent.$("iframe").hide();
    window.parent.location.href = ruta + ".jsp?identificador=" + identificador;
}

function hv_r(ruta, contenedor, identificador) {
    window.parent.$("iframe").animate({
        scrollTop: 0
    }, 500);
    window.parent.$(".gif_cargando").show();
    window.parent.$(".div_container_principal").hide();
    location.href = ruta + ".jsp?identificador=" + identificador;
}
/*Fin funcion para mostrar hoja de vida*/
/*Inicio funcion change content*/
function change_content(ruta, contenedor, id) {
    if (id == null) id = 0;
    window.parent.$(".gif_cargando").show();
    window.parent.$("iframe").hide();
    location.href = ruta + ".jsp?identificador=" + id;
    //console.log("history " + ruta + '.jsp data: 0 title:' + ruta + '.jsp');
}
/*Fin funcion change content*/
/*Fin funciones index*/
/*Inicio funciones hv*
//Inicio funcion para que no seadmitan caracteres extraños en ningun campo
var a = new RegExp('[^ 0-9a-zA-Z]', 'g');
$('input').on('input', function() {
    $(this).val($(this).val().replace(a, ''));
});*/
//Fin funcion para que no seadmitan caracteres extraños
//Inicio funcion para que en los campos de texto no se admitan numeros
function validar(e) {
    key = e.keyCode || e.which;
    tecla = String.fromCharCode(key).toLowerCase();
    letras = " áéíóúabcdefghijklmnñopqrstuvwxyz1234567890_."; //estos son los caracteres que va a aceptar
    especiales = "8-37-39-46";
    enter = "13";
    tecla_especial = false
    for (var i in especiales) {
        if (key == especiales[i]) {
            tecla_especial = true;
            break;
        }
        if (key == enter) {
            tecla_especial = true;
            break;
        }
    }
    if (letras.indexOf(tecla) == -1 && !tecla_especial) {
        return false;
    }
}
//Fin funcion para que en los campos de texto no se admitan numeros
/*Inicio Funcion para envio de formulario hoja de vida*/
$("#form_hv").submit(function(event) {
    if ($("#tp_dato").val().length > 0 || $("#valor_dato").val().length > 0) {
        if ($("#valor_dato").val().length > 0 && $("#tp_dato").val().length < 1) {
            $(".falta_tp_dato").slideDown();
            $(".falta_dato").slideUp();
            $("html").animate({
                scrollTop: 300
            }, 500);
            event.preventDefault();
        } else if ($("#valor_dato").val().length < 1 && $("#tp_dato").val().length > 0) {
            $(".falta_dato").slideDown();
            $(".falta_tp_dato").slideUp();
            $("html").animate({
                scrollTop: 300
            }, 500);
            event.preventDefault();
        } else {
            $(".falta_tp_dato").slideUp();
            $(".falta_dato").slideUp();
            window.parent.$(".gif_cargando").show();
            window.parent.$("iframe").hide();
            $("#form_hv").submit();
        }
    } else {
        $(".falta_tp_dato").slideUp();
        $(".falta_dato").slideUp();
        window.parent.$(".gif_cargando").show();
        window.parent.$("iframe").hide();
        $("#form_hv").submit();
    }
    event.preventDefault();
});
/*Fin Funcion para envio de formulario hoja de vida*/
$("select[name=asunto_crear_text]").change(function() {
    // alert("adgfasdfgsdgsdfk");
    $("#asunto_crear").val($('select[name=asunto_crear_text]').val());
});
$("#form_crear_tickets").submit(function(event) {
    if ($("#descripsion").val().length < 1 || $("#prioridad_crear").val().length < 1) {
        event.preventDefault();
        $(".advertencia").slideDown();
        $("body").animate({
            scrollTop: 0
        }, 500);
    } else {
        $(".advertencia").slideUp();
        var url = "validacion_crear_tickets.jsp"
        $.ajax({
            type: "POST",
            url: url,
            data: $("#form_crear_tickets").serialize(),
            success: function(datos) {
                $("#asunto_crear_id").val("");
                $("#prioridad_crear").val("");
                $("#descripsion").val("");
                $('.validacion_tickets').html(datos);
                var a = $('body').height() + 20;
                var x = a * 45 / 100;
                //alert(x);
                parent.$('body').animate({
                    scrollTop: x
                }, 500);
            }
        });
    }
    event.preventDefault();
});
$("#form_tickets_pc").submit(function(event) {
    if ($("#ticket_id").val().length < 1 && $("#select").val().length < 1 && $("#proceso_id").val().length < 1 && $("#plazo").val().length < 1 && $("#asunto_cerrado").val().length < 1 && $("#prioridad").val().length < 1) {
        event.preventDefault();
        $(".advertencia_pc").slideDown();
        $('.validacion_tickets_busqueda').hide();
    } else {
        $(".advertencia_pc").slideUp();
        window.parent.$(".gif_cargando").show();
        window.parent.$("iframe").hide();
        $("#form_tickets_pc").submit();
    }
    event.preventDefault();
});
/*Fin funciones hv*/
/*Inicio de funciones para busqueda rapida por proceso*/
$("#busqueda_por_proceso_rapido").submit(function(event) {
    if ($("#identificacionInput").val().length < 2) {
        swal({
            title: "¡¡Ooooops!!",
            text: "Para realizar una busqueda rapida por identificador debe ingresar un valor",
            type: "warning",
            showConfirmButton: true,
            showCancelButton: false,
            confirmButtonColor: '#42547f',
            confirmButtonText: "Entendido",
            closeOnConfirm: true,
            closeOnCancel: true
        });
        event.preventDefault();
    } else {
        //parent.$('.container_busca_p_id').hide();
        $("#busqueda_por_proceso_rapido").submit();
    }
    event.preventDefault();
});
/*Inicio de funciones para validar cuando genera el informe de rango de fechas*/
$("#rango_fechas").submit(function(event) {
    if ($("#rango_ini").val().length < 1 || $("#rango_fin").val().length < 1) {
        error();
    } else {
        // window.open('about:blank', 'width=1000,height=800');
        $("#rango_fechas").submit();
    }
    event.preventDefault();
});
/*Fin de funciones para validar cuando genera el informe de rango de fechas*/
/*Fin de funciones para busqueda rapida por proceso*/
$("#form_crear_anotacion").submit(function(event) {
    if ($("#anotacion").val().length < 1) {
        event.preventDefault();
        $(".advertencia_an").slideDown();
    } else {
        $(".advertencia_an").slideUp();
        window.parent.$(".gif_cargando").show();
        window.parent.$("iframe").hide();
        var url = "anotaciones_validacion.jsp"
        $.ajax({
            type: "POST",
            url: url,
            data: $("#form_crear_anotacion").serialize(),
            success: function(datos) {
                window.parent.$(".gif_cargando").hide();
                window.parent.$("iframe").show();
                $('#crear_anotacion').html(datos);
            }
        });
    }
    event.preventDefault();
});
/*Inicio funcion para mostrar contenedor buscador rapido*/
$(document).ready(function() {
        //Esta funcion es para retrasar 1 seg el calcular top y left del buscador rapido
        setTimeout(function() {
            //
            var a = $('nav').height();
            var b = $('#busca_p_id').position();
            //b = b.left;
            //alert(b);
            $('.container_busca_p_id').css({
                "top": a,
                "left": b
            });
        }, 1000);
    $('#busca_p_id').click(function() {
        $('.container_busca_p_id').slideToggle();
    });
});
/*Fin funcion para mostrar contenedor buscador rapido*/

$(document).ready(function() {
    var msgRadicacion = new Vue({
      el: '#msg-radicacion',
      data: {
        message: 'Usted está utlizando el módulo Radicaciones'
      }
    })
});
