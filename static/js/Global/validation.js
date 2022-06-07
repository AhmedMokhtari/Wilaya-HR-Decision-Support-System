$('input[name=password]').on('change invalid', function() {
        var textfield = $(this).get(0);
        textfield.setCustomValidity('');

        if (!textfield.validity.valid) {
          textfield.setCustomValidity('الرقم السري يجب أن يحتوي على 8 حروف وأرقام');
        }
    });


    $('input[type=text]').add('input[type=date]').add('input[type=number]').on('change invalid', function() {
        var textfield = $(this).get(0);
        textfield.setCustomValidity('');

        if (!textfield.validity.valid) {
          textfield.setCustomValidity('يرجى ملء هذا الحقل');
        }
    });