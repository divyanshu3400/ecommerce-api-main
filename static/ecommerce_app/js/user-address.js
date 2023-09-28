$(document).ready(function () {
  $('#button_update').hide();
  $('#addBtn').show();
  $('#error').hide();
  $('#success').hide();
  $("#addForm").hide();
  $('#error').hide();
  $('#stateDropdown').select2();

  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        // Check if this cookie name matches the format we expect for the CSRF token
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  // Add CSRF token to all AJAX requests
  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      // Check if the request method is safe (e.g., GET, HEAD, OPTIONS)
      if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
        // Add the CSRF token to the request headers
        xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
      }
    }
  });

  $.ajax({
    url: getStatesUrl,
    success: function (state) {
      $.each(state, function (index, state) {
        var option = $('<option>', {
          value: state.name,
          text: state.name
        }).data('ids', state.id);
        $('#stateDropdown').append(option);
      });
    }
  });

  // When the state dropdown value changes
  $('#stateDropdown').on('change', function () {
    event.preventDefault();
    var selectedStateOption = $('#stateDropdown option:selected');
    var selectedState = selectedStateOption.data('ids');
    if (selectedState) {
      // Fetch cities based on the selected state
      fetchCities(selectedState);
    } else {

      // If no state is selected, clear the city dropdown
      $('#cityDropdown').empty().trigger('change');
    }
  });

  // Function to fetch cities based on the selected state
  function fetchCities(selectedState) {
    // Send an AJAX request to fetch cities based on the selected state
    $.ajax({
      url: getCitiesUrl,
      data: { "state": selectedState },
      success: function (data) {
        // Clear the existing city options
        $('#cityDropdown').empty();
        // $('#cityDropdown').append('<option value="">District</option>')
        // Populate the city options with the fetched data
        $.each(data, function (index, city) {
          var option = $('<option>', {
            value: city.name,
            text: city.name
          });
          $('#cityDropdown').append(option);
        });

        // Trigger the change event to update Select2 after populating the cities
        $('#cityDropdown').trigger('change');
      }
    });
  }


  $('#stateDropdown').select2({
    placeholder: 'Search for a state',
    allowClear: true,
    minimumInputLength: 1
  });

  $('#cityDropdown').select2({
    placeholder: 'Search for a district',
    allowClear: true,
    minimumInputLength: 1
  });

  $('#addressForm').submit(function (event) {
    event.preventDefault();
    console.log($('#stateDropdown').val());
    var address = $(this).serialize();
    $.ajax({
      url: manageAddressUrl,
      method: 'POST',
      data: address,

      success: function (response) {
        if (response.success) {
          $('#success').show();
          $("#success").html('<i class="fa fa-times-circle"></i> ' + response.message);
          refreshManageAddress();
        } else {
          $('#error').show();
          $("#error").html('<i class="fa fa-times-circle"></i> ' + response.message);
        }
      },

      error: function (xhr, errmsg, err) {
        $('#error').show();
        $("#error").html('<i class="fa fa-times-circle"></i> ' + "Fields are required !!");
      },

      complete: function () {
        // Re-enable the submit button and hide the loader
        $('#btnChangePassword').prop('disabled', false);
        $('#loader').hide();
        $('#buttonText').show();
      }
    });
  });
});

function deleteAddress(addressId) {
  // Open the custom dialog popup
  $('#deleteAddressModal').modal('show');
  // Store the address ID in a data attribute of the delete button
  $('#confirmDeleteBtn').data('address-id', addressId);
}

function editAddress(button) {
  $("#addForm").show();
  $('#button_update').show();
  $('#addBtn').hide();
  $('#updateAddressBtn').data('id', $(button).data('id'));
  // Set address data in form fields
  $('#id_address_line_1').val($(button).data('address-line-1'));
  $('#id_address_line_2').val($(button).data('address-line-2'));
  $('#id_postal_code').val($(button).data('postal-code'));
  $('#id_country').val($(button).data('country'));
  // Set state dropdown
  // $('#stateDropdown').val($(button).data('state'));
  // $('#cityDropdown').empty().trigger('change');
  // $('#stateDropdown').trigger('change');
  // Check if any option text matches the cityName
  var cityName = $(button).data('city');
  console.log(cityName);
  $('#cityDropdown').val(cityName);
  $('#cityDropdown').trigger('change');

  $('#updateAddressBtn').on('click', function () {
    updateAddress();
  });

};

// Handle the delete button click event in the custom dialog
$('#confirmDeleteBtn').on('click', function () {
  var addressId = $(this).data('address-id');  // Retrieve the address ID from the data attribute

  $.ajax({
    type: 'POST',
    url: deleteAddressUrl,  // Replace with the actual URL for deleting the address
    data: {
      "id": addressId,
    },
    success: function (response) {
      if (response.success) {
        $('#address-' + addressId).remove();
        $('#success').show();
        $("#success").html('<i class="fa fa-times-circle"></i> ' + response.message);
        refreshManageAddress();
      }
      else {
        $('#error').show();
        $("#error").html('<i class="fa fa-times-circle"></i> ' + response.message);
      }
    },
    error: function (xhr, textStatus, errorThrown) {
      console.error('Error: ' + errorThrown);
    }
  });
  // Close the custom dialog popup
  $('#deleteAddressModal').modal('hide');
});

$('#cancelButton').click(function () {
  $('#deleteAddressModal').modal('hide');
})

function refreshManageAddress() {
  $.ajax({
    url: manageAddressUrl,  // Replace with the actual URL for fetching the updated manage-address content
    method: 'GET',
    success: function (response) {
      // Update the content of the 'manage-address' section with the updated HTML
      $('#manage-address').html(response);
    },
    error: function (xhr, textStatus, errorThrown) {
      console.error('Error: ' + errorThrown);
    }
  });
}

function showForm() {
  $("#addForm").show();
}

function updateAddress() {
  console.log("Update Button Clicked")
  var addressId = $(this).data('id');
  // Serialize all the form fields into an array of objects
  var formDataArray = $('#addressForm').serializeArray();

  var formData = {};
  $.each(formDataArray, function (index, field) {
    formData[field.name] = field.value;
  });
  formData['id'] = addressId;
  console.log(formData);

  $.ajax({
    url: updateAddressUrl,
    method: 'POST',
    data: formData,

    success: function (response) {
      if (response.success) {
        console.log(response.success)
        $('#success').show();
        $("#success").html('<i class="fa fa-times-circle"></i> ' + response.message);
        refreshManageAddress();
      } else {
        $('#error').show();
        $("#error").html('<i class="fa fa-times-circle"></i> ' + response.message);
      }
    },

    error: function (xhr, errmsg, err) {
      console.log(errmsg)
      $('#error').show();
      $("#error").html('<i class="fa fa-times-circle"></i> ' + "Fields are required !!");
    },

    complete: function () {
      console.log("Complete")
      // Re-enable the submit button and hide the loader
      $('#saveAddressBtn').prop('disabled', false);
      $('#loader').hide();
      $('#buttonText').show();
    }
  });

}