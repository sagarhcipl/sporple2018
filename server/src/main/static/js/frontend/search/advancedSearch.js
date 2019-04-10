$(document).ready(function() {
    var initialSelectedSport = $('#sport-select').val();
    $('#position-select-' + initialSelectedSport).show();

    $('#sport-select').on('change', function (e) {
        var selectedSport = $(this).val();

        $('.position-select').val(null);
        $('ul.positions').empty();
        $('.position-select').not('#position-select-' + selectedSport).hide();
        $('#position-select-' + selectedSport).show();
    });

    $('.position-select').on('change', function (e) {
        var selectedSport = $(this).val(),
            selectedPositions = $('ul.positions');

        if (selectedPositions.find('input[value="' + selectedSport + '"]').length === 0) {
            selectedPositions.append(
                '<li>' +
                    '<input type="hidden" name="positions[]" value="' + selectedSport + '"/>' +
                    '<button type="button" class="options-reset" onclick="$(this).closest(\'li\').remove();"></button>' +
                    selectedSport +
                '</li>'
            );
        }

        $(this).val(null);
    });

    $('.country-select').on('change', function (e) {
        var selectedCountry = $(this).val();

        $('ul.countries').append(
            '<li>' +
                '<input type="hidden" name="countries[]" value="' + selectedCountry + '"/>' +
                '<button type="button" class="options-reset" onclick="$(this).closest(\'li\').remove();"></button>' +
                selectedCountry +
            '</li>'
        );
        $(this).val(null);
    });

    $('.passport-select').on('change', function (e) {
        var selectedCountry = $(this).val();

        $('ul.passports').append(
            '<li>' +
                '<input type="hidden" name="passports[]" value="' + selectedCountry + '"/>' +
                '<button type="button" class="options-reset" onclick="$(this).closest(\'li\').remove();"></button>' +
                selectedCountry +
            '</li>'
        );
        $(this).val(null);
    });

    $('button.reset-panel[type="reset"]').on('click', function () {
        var target = $(this).data('target');

        if (target === 'age' || target === 'weight' || target === 'height') {
            $('min-'+target+'-select').val(null);
            $('max-'+target+'-select').val(null);
        } else {
            $('ul.'+target).empty();
        }
    });
});
