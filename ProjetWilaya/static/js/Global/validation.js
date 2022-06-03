$('input[name=password]').on('change invalid', function() {
        var textfield = $(this).get(0);
        textfield.setCustomValidity('');

        if (!textfield.validity.valid) {
          textfield.setCustomValidity('الرقم السري يجب أن يحتوي على 8 حروف وأرقام');
        }
    });

    $('input[type=text]').on('change invalid', function() {
        var textfield = $(this).get(0);
        textfield.setCustomValidity('');

        if (!textfield.validity.valid) {
          textfield.setCustomValidity('يرجى ملء هذا الحقل');
        }
    });