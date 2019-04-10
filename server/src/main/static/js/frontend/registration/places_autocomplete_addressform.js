function athlete_geolocate() {
    var componentForm = {
        locality: {
            id: 'registration_address_city',
            element: 'long_name'
        },
        country: {
            id: 'registration_address_country_id',
            element: 'long_name'
        }
    };
    geolocate(componentForm);

    $('#registration_form').submit(function(e) {
        if ($('#' + componentForm['locality'].id).val() === '') {
            var countryVal = $('#' + componentForm['country'].id + ' option:selected').text(),
                cityVal = $('#autocomplete').val().replace(", " + countryVal, "");

            $('#' + componentForm['locality'].id).val(cityVal);
        }
    });
}

function agent_geolocate() {
    var componentForm = {
        country: {
            id: 'registration_address_country_id',
            element: 'long_name'
        }
    };
    geolocate(componentForm);
}


function club_geolocate() {
    var componentForm = {
        country: {
            id: 'registration_address_country_id',
            element: 'long_name'
        },
        postal_code: {
            id: 'registration_address_zipcode',
            element: 'long_name'
        },
        route: {
            id: 'registration_address_street',
            element: 'long_name'
        },
        sublocality: {
            id: 'registration_address_suburb',
            element: 'long_name'
        }
    };

    geolocate(componentForm);
}

function initialize(componentForm) {
    // Create the autocomplete object, restricting the search
    // to geographical location types.
    autocomplete = new google.maps.places.Autocomplete(
        /** @type {HTMLInputElement} */(document.getElementById('autocomplete')),
        { types: ['geocode'] });
    // When the user selects an address from the dropdown,
    // populate the address fields in the form.
    google.maps.event.addListener(autocomplete, 'place_changed', function () {
        fillInAddress(componentForm);
    });
}

// [START region_fillform]
function fillInAddress(componentForm) {
    // Get the place details from the autocomplete object.
    var place = autocomplete.getPlace();

    for (component in componentForm) {
        var element = $('#' + componentForm[component].id);
        element.value = '';
        element.disabled = false;
    }

    // Get each component of the address from the place details
    // and fill the corresponding field on the form.
    for (var i = 0; i < place.address_components.length; i++) {
        var addressType = place.address_components[i].types[0];

        if (typeof componentForm[addressType] !== 'undefined') {
            var address_component = $('#' + componentForm[addressType].id);

            if (address_component.length !== 0) {
                var val = place.address_components[i][componentForm[addressType].element];

                if (address_component.is("select")) {
                    address_component.find("option").filter(function (index) {
                        return val === $(this).text();
                    }).prop("selected", "selected");
                } else {
                    address_component.val(val);
                }

            }

        }

    }
}
// [END region_fillform]

// [START region_geolocation]
// Bias the autocomplete object to the user's geographical location,
// as supplied by the browser's 'navigator.geolocation' object.
function geolocate(componentForm) {
    if (navigator.geolocation) {
        initialize(componentForm);
    }
}
// [END region_geolocation]
