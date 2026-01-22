var options, a;
    jQuery(function () {
        options = { serviceUrl: './Autocomplete.ashx' };
        a = $('#ctl00_BodyContentPlaceholder_txtEmail').autocomplete(options);
    });