funcion(fabrica, jQuery, Zepto) {
if (typeof define === 'function' && define.amd) {
    define(['jquery'], factory);
} else if (tipo de exportaciones === 'objeto') {
    module.exports = factory(require('jquery'));
} else {
    fabrica(jQuery || Zepto);
}
}(funcion($) {
var Mascara = funcion(el, mascara, opciones) {
    var p = {
        invalido: [],
        getCaret: function() {
            tratar {
                var sel
                pos = 0,
                    ctrl = el.get(0),
                    dSel = document.selection,
                    cSelStart = ctrl.selectionStart;
                // Soporte de IE
                if (dSel && navigator.appVersion.indexOf('MSIE 10') === -1) {
                    sel = dSel.createRange();
                    sel.moveStart('caracter', -p.val().longitud);
                    pos = sel.text.length;
                }
                // soporte para Firefox
                mas si(cSelStart || cSelStart === '0') {
                    pos = cSelStart;
                }
                retorno pos;
            }
            atrapar(e) {}
        }
        setCaret: function(pos) {
            tratar {
                if (el.is(': focus')) {
                    var range, ctrl = el.get(0);
                    // Firefox, WebKit, etc.
                    if (ctrl.setSelectionRange) {
                        ctrl.setSelectionRange(pos, pos);
                    } else { // IE
                        range = ctrl.createTextRange();
                        range.collapse(true);
                        range.moveEnd('caracter', pos);
                        range.moveStart('caracter', pos);
                        range.select();
                    }
                }
            }
            atrapar(e) {}
        }
        eventos: function() {
            el.on('keydown.mask', funcion(e) {
                    el.data('mask-keycode', e.keyCode || e.which);
                    el.data('mask-previus-value', el.val());
                }).on($.jMaskGlobals.useInput ? 'input.mask' : 'keyup.mask', p.behaviour).on('paste.mask drop.mask', function() {
                    setTimeout(function() {
                        el.keydown().keyup();
                    }, 100);
                }).on('change.mask', function() {
                    el.data('cambiado', verdadero);
                }).on('blur.mask', function() {
                    if (oldValue! == p.val() && !el.data('cambiado')) {
                        el.trigger('cambio');
                    }
                    el.data('cambiado', falso);
                })
                // es muy importante que esta devolucion de llamada permanezca en esta posicion
                // otrowhise oldValue va a funcionar en buggy
                .on('blur.mask', function() {
                    valor antiguo = p.val();
                })
                // seleccionar todo el texto en foco
                .on('focus.mask', function(e) {
                    if (options.selectOnFocus === true) {
                        $(e.target).select();
                    }
                })
                // borrar el valor si no completa la mascara
                .on('focusout.mask', function() {
                    if (options.clearIfNotMatch && !regexMask.test(p.val())) {
                        p.val('');
                    }
                });
        }
        getRegexMask: function() {
            var maskChunks = [],
                traduccion, patron, opcional, recursivo, oRecursivo, r;
            para(var i = 0; i < mask.length; i++) {
                traduccion = jMask.translation[mask.charAt(i)];
                if (traduccion) {
                    pattern = translation.pattern.toString().replace(/. {1} $ | ^. {1} /
                        g, '');
                    opcional = traduccion.opcional;
                    recursivo = traduccion.recursivo;
                    si(recursivo) {
                        maskChunks.push(mask.charAt(i));
                        oRecursive = {
                            digit: mask.charAt(i),
                            pattern: pattern
                        };
                    } else {
                        maskChunks.push(!opcional && !recursive ? patron : (patron + '?'));
                    }
                } else {
                    maskChunks.push(mask.charAt(i).replace(/ [- \ / \\ ^ $ * +? () | [\] {}] /
                        g, '\\ $ &'));
                }
            }
            r = maskChunks.join('');
            si(oRecursivo) {
                r = r.replace(new RegExp('(' + oRecursive.digit + '(. *' + oRecursive.digit + ')?)'), '($ 1)?').replace(nuevo RegExp(oRecursive.digit, 'g'), oRecursive.pattern);
            }
            devolver nuevo RegExp(r);
        }
        destroyEvents: function() {
            el.off(['input', 'keydown', 'keyup', 'paste', 'drop', 'blur', 'focusout', ''].join('. mask'));
        }
        val: funcion(v) {
            var isInput = el.is('input'),
                method = isInput ? 'val' : 'texto',
                r;
            if (argumentos.longitud > 0) {
                if (el[method]() ! == v) {
                    el[método](v);
                }
                r = el;
            } else {
                r = el[método]();
            }
            volver r;
        }
        CalculateCaretPosition: function(caretPos, newVal) {
            var newValL = newVal.length,
                oValue = el.data('mask-previus-value') || '',
                oValueL = oValue.length;
            // casos de borde al borrar dígitos
            if (el.data('mask-keycode') === 8 && oValue! == newVal) {
                caretPos = caretPos - (newVal.slice(0, caretPos).length - oValue.slice(0, caretPos).length);
                // casos de borde al escribir nuevos dígitos
            } else if (oValue! == newVal) {
                // Si el cursor esta al final, mantenlo ahí.
                if (caretPos > = oValueL) {
                    caretPos = newValL;
                } else {
                    caretPos = caretPos + (newVal.slice(0, caretPos).length - oValue.slice(0, caretPos).length);
                }
            }
            devuelve caretPos;
        }
        comportamiento: funcion(e) {
            e = e || window.event;
            p.invalid = [];
            var keyCode = el.data('mask-keycode');
            if ($.inArray(keyCode, jMask.byPassKeys) === -1) {
                var newVal = p.getMasked(),
                    caretPos = p.getCaret();
                setTimeout(funcion(caretPos, newVal) {
                    p.setCaret(p.calculateCaretPosition(caretPos, newVal));
                }, 10, caretPos, newVal);
                p.val(newVal);
                p.setCaret(caretPos);
                devuelve p.callbacks(e);
            }
        }
        getMasked: function(skipMaskChars, val) {
            var buf = [],
                valor = val === indefinido ? p.val() : val + '',
                m = 0,
                maskLen = mask.length,
                v = 0,
                valLen = value.length,
                offset = 1,
                addMethod = 'push',
                resetPos = -1,
                lastMaskChar,
                comprobar;
            if (options.reverse) {
                addMethod = 'unshift';
                desplazamiento = -1;
                lastMaskChar = 0;
                m = maskLen - 1;
                v = valLen - 1;
                check = function() {
                    devuelve m > -1 && v > -1;
                };
            } else {
                lastMaskChar = maskLen - 1;
                check = function() {
                    devolver m < maskLen && v < valLen;
                };
            }
            var lastUntranslatedMaskChar;
            while (check()) {
                var maskDigit = mask.charAt(m),
                    valDigit = value.charAt(v),
                    translation = jMask.translation[maskDigit];
                if (traduccion) {
                    if (valDigit.match(translation.pattern)) {
                        buf[addMethod](valDigit);
                        if (translation.recursive) {
                            if (resetPos === -1) {
                                resetPos = m;
                            } else if (m === lastMaskChar) {
                                m = resetPos - offset;
                            }
                            if (lastMaskChar === resetPos) {
                                m - = desplazamiento;
                            }
                        }
                        m + = desplazamiento;
                    } else if (valDigit === lastUntranslatedMaskChar) {
                        // coincidio con el último caracter de mascara no traducida (sin formato) que encontramos
                        // es probable que una insercion desplace el caracter de mascara de la última entrada; otoño
                        // a través y solo incremento v
                        lastUntranslatedMaskChar = undefined;
                    } else if (translation.optional) {
                        m + = desplazamiento;
                        v - = desplazamiento;
                    } else if (translation.fallback) {
                        buf[addMethod](translation.fallback);
                        m + = desplazamiento;
                        v - = desplazamiento;
                    } else {
                        p.invalid.push({
                            p: v,
                            v: valDigit,
                            e: translation.pattern
                        });
                    }
                    v + = desplazamiento;
                } else {
                    if (!skipMaskChars) {
                        buf[addMethod](maskDigit);
                    }
                    if (valDigit === maskDigit) {
                        v + = desplazamiento;
                    } else {
                        lastUntranslatedMaskChar = maskDigit;
                    }
                    m + = desplazamiento;
                }
            }
            var lastMaskCharDigit = mask.charAt(lastMaskChar);
            if (maskLen === valLen + 1 && !jMask.translation[lastMaskCharDigit]) {
                buf.push(lastMaskCharDigit);
            }
            devuelve buf.join('');
        }
        devoluciones de llamada: funcion(e) {
            var val = p.val(),
                cambiado = val! == oldValue,
                defaultArgs = [val, e, el, options],
                callback = funcion(nombre, criterios, argumentos) {
                    if (typeof options[nombre] === 'funcion' && criterios) {
                        opciones[nombre].apply(esto, args);
                    }
                };
            devolucion de llamada('onChange', cambiado === true, defaultArgs);
            devolucion de llamada('onKeyPress', cambiado === true, defaultArgs);
            devolucion de llamada('onComplete', val.length === mask.length, defaultArgs);
            devolucion de llamada('onInvalid', p.invalid.length > 0, [val, e, el, p.invalid, opciones]);
        }
    };
    el = $(el);
    var jMask = this,
        oldValue = p.val(),
        regexMask;
    mask = typeof mask === 'function' ? mask(p.val(), undefined, el, options) : mask;
    // métodos públicos
    jMask.mask = mascara;
    jMask.options = opciones;
    jMask.remove = function() {
        var caret = p.getCaret();
        p.destroyEvents();
        p.val(jMask.getCleanVal());
        p.setCaret(caret);
        volver el;
    };
    // obtener valor sin mascara
    jMask.getCleanVal = function() {
        return p.getMasked(true);
    };
    // obtener valor enmascarado sin que el valor esté en la entrada o elemento
    jMask.getMaskedVal = function(val) {
        devuelve p.getMasked(false, val);
    };
    jMask.init = function(onlyMask) {
        onlyMask = onlyMask || falso;
        opciones = opciones || {};
        jMask.clearIfNotMatch = $.jMaskGlobals.clearIfNotMatch;
        jMask.byPassKeys = $.jMaskGlobals.byPassKeys;
        jMask.translation = $.extend({}, $.jMaskGlobals.translation, options.translation);
        jMask = $.extend(true, {}, jMask, opciones);
        regexMask = p.getRegexMask();
        if (onlyMask) {
            p.eventos();
            p.val(p.getMasked());
        } else {
            if (options.placeholder) {
                el.attr('placeholder', options.placeholder);
            }
            // esto es necesario, de lo contrario si el usuario envía el formulario
            // y luego presione el boton "atras", el autocompletar borrara
            // los datos. Funciona bien en IE9 +, FF, Opera, Safari.
            if (el.data('mask')) {
                el.attr('autocompletar', 'apagar');
            }
            // Detectar si es necesario dejar que el usuario escriba libremente.
            // for es mucho mas rapido que forEach.
            para(var i = 0, maxlength = true; i < mask.length; i++) {
                traduccion de
                var = jMask.translation[mask.charAt(i)];
                if (translation && translation.recursive) {
                    maxlength = falso;
                    descanso;
                }
            }
            si(longitud maxima) {
                el.attr('maxlength', mask.length);
            }
            p.destroyEvents();
            p.eventos();
            var caret = p.getCaret();
            p.val(p.getMasked());
            p.setCaret(caret);
        }
    };
    jMask.init(!el.is('input'));
};
$.maskWatchers = {};
var HTMLAttributes = function() {
    var input = $(esto),
        opciones = {},
        prefijo = 'mascara de datos-',
        mask = input.attr('data-mask');
    if (input.attr(prefijo + 'invertir')) {
        options.reverse = true;
    }
    if (input.attr(prefijo + 'clearifnotmatch')) {
        options.clearIfNotMatch = true;
    }
    if (input.attr(prefijo + 'selectonfocus') === 'true') {
        options.selectOnFocus = true;
    }
    if (notSameMaskObject(entrada, mascara, opciones)) {
        return input.data('mascara', nueva mascara(esto, mascara, opciones));
    }
}
notSameMaskObject = function(field, mask, options) {
    opciones = opciones || {};
    var maskObject = $(field).data('mask'),
        stringify = JSON.stringify,
        valor = $(campo).val() || $(campo).text();
    tratar {
        if (typeof mask === 'function') {
            mascara = mascara(valor);
        }
        devuelve typeof maskObject! == 'object' || stringify(maskObject.options) ! == stringify(opciones) || maskObject.mask! == mask;
    }
    atrapar(e) {}
}
eventSupported = function(eventName) {
    var el = document.createElement('div'),
        isSupported;
    eventName = 'on' + eventName;
    isSupported = (eventName en el);
    if (!isSupported) {
        el.setAttribute(eventName, 'return;');
        isSupported = typeof el[eventName] === 'function';
    }
    el = nulo;
    el retorno es Compatible;
};
$.fn.mask = function(mascara, opciones) {
    opciones = opciones || {};
    selector de
    var = this.selector,
        globals = $.jMaskGlobals,
        intervalo = globals.watchInterval,
        watchInputs = options.watchInputs || globals.watchInputs,
        maskFunction = function() {
            if (notSameMaskObject(this, mask, options)) {
                devuelve $(this).data('mascara', nueva mascara(esta, mascara, opciones));
            }
        };
    $(este).each(maskFunction);
    if (selector && selector! == '' && watchInputs) {
        clearInterval($.maskWatchers[selector]);
        $.maskWatchers[selector] = setInterval(function() {
            $(documento).find(selector).each(maskFunction);
        }, intervalo);
    }
    devuelve esto
};
$.fn.masked = function(val) {
    devuelve this.data('mascara').getMaskedVal(val);
};
$.fn.unmask = function() {
    clearInterval($.maskWatchers[this.selector]);
    eliminar $.maskWatchers[this.selector];
    devuelve this.each(function() {
        var dataMask = $(this).data('mask');
        if (dataMask) {
            dataMask.remove().removeData('mask');
        }
    });
};
$.fn.cleanVal = function() {
    devuelve this.data('mascara').getCleanVal();
};
$.applyDataMask = function(selector) {
    selector = selector || $.jMaskGlobals.maskElements;
    var $ selector = (selector instanceof $) ? selector : $(selector);
    $ selector.filter($.jMaskGlobals.dataMaskAttr).each(HTMLAttributes);
};
var globals = {
    maskElements: 'input, td, span, div',
    dataMaskAttr: '* [data-mask]',
    DataMask: verdadero,
    watchInterval: 300,
    watchInputs: verdadero,
    // las versiones antiguas de Chrome no funcionan muy bien con un evento de entrada
    useInput: !/ Chrome \ / [2 - 4][0 - 9] | SamsungBrowser / .test(window.navigator.userAgent) && eventSupported('input'),
    watchDataMask: falso,
    byPassKeys: [9, 16, 17, 18, 36, 37, 38, 39, 40, 91],
    traduccion: {
        '0': {
            patron: / \ d /
        },
        '9': {
            patron: / \ d /,
            opcional: verdadero
        },
        '#': {
            patron: / \ d /,
            recursivo: verdadero
        },
        'A': {
            patron: / [a-zA-Z0-9] /
        },
        'S': {
            patron: / [a-zA-Z] /
        }
    }
};
$.jMaskGlobals = $.jMaskGlobals || {};
globals = $.jMaskGlobals = $.extend(true, {}, globals, $.jMaskGlobals);
// buscando entradas con atributo de mascara de datos
if (globals.dataMask) {
    $.applyDataMask();
}
setInterval(function() {
    if ($.jMaskGlobals.watchDataMask) {
        $.applyDataMask();
    }
}, globals.watchInterval);
}, window.jQuery, window.Zepto));
