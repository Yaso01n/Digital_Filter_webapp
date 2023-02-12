
(function () {
  let allpassfilterzplanecanvas = document.getElementById("allpasszplane");
  let allpassfilterzplanectx = allpassfilterzplanecanvas.getContext("2d");
  let w;
  let magnitude;
  let angle;
  let zeros = [];
  let poles = [];
  let library = [];
  let avalues = [];
  let allpassfilters = [];
  let flag = true;

  function combobox() {
    library.forEach(function (element, index) {
      $('#a-values').append(`<option value="${index}">${element}</option>`);
    });
  }
  $.ajax({
    url: '/updatelibrary',
    type: 'get',
    success: function (response) {
      library = response;
      combobox();
      drawfrequencyreposne([], [], [], 'allpassfrequencyresponse', 'Magnitude', 'Phase');
      drawPlane(allpassfilterzplanectx);
    }
  });
  function updataAllpassFilterFrequencyResponse() {
    $.ajax({
      url: '/sendallpassfilter',
      type: 'get',
      success: function (response) {
        data = response;
        zeros = data.zeros
        poles = data.poles
        magnitude = data.magnitude;
        w = data.w;
        angle = data.angle;
        library = data.library;
        allpassfilterzplanectx.clearRect(0, 0, cw, ch);
        drawAll(allpassfilterzplanectx, zeros, poles,'#291919');
        drawfrequencyreposne(w, magnitude, angle, 'allpassfrequencyresponse', 'Magnitude', 'Phase');
        drawPlane(allpassfilterzplanectx);
      }
    });

  }
  $('#a-values').change(function () {
    let index = $(this).val();
    let js_index = JSON.stringify(index);
    $('#addFilterLoader').html('');
    $.ajax({
      url: '/getallpassfilter',
      type: 'post',
      contentType: 'application/json',
      dataType: 'json',
      data: js_index,
      success: function () {
        updataAllpassFilterFrequencyResponse();
      }
    });
  });

  function addaValues() {
    let vals = [...document.getElementsByClassName('allpassfiltera')]
    vals.forEach(function (element) {
      avalues.push(element.value);
    });
  }

  function validate(arr) {
    if (arr[0] == '' || arr[1] == '') {
      $(".allpassfiltera").addClass("invalid");
      $(".allpassfiltera").removeClass("valid");
      $('#addfiltertolibrary').prop('disabled', true);
      avalues = [];
      return false;
    }
    if (arr[0] > 1.5 || arr[1] > 1.5 || arr[0] < -1.5 || arr[1] < -1.5) {
      $(".allpassfiltera").addClass("invalid");
      $(".allpassfiltera").removeClass("valid");
      $('#addfiltertolibrary').prop('disabled', true);
      avalues = [];
      return false;

    }
    $(".allpassfiltera").addClass("valid");
      $(".allpassfiltera").removeClass("invalid");
      $('#addfiltertolibrary').prop('disabled', false);
    avalues = [parseFloat(arr[0]), parseFloat(arr[1])];
    return true;
  }

  function updatelibrary() {
    $.ajax({
      url: '/updatelibrary',
      type: 'get',
      success: function (response) {
        library = response;
        $('#addFilterToLibraryLoader').html('<i class="fas fa-check"></i>');
        $('#a-values').append(`<option value="${library.length-1}" selected="selected">${library[library.length-1]}</option>`);
        allpassfilterzplanectx.clearRect(0, 0, cw, ch);
        drawAll(allpassfilterzplanectx, zeros, poles,'#291919');
        drawfrequencyreposne(w, magnitude, angle, 'allpassfrequencyresponse', 'Magnitude', 'Phase');
        drawPlane(allpassfilterzplanectx);
      }
    });
  }

  $('.allpassfiltera').keyup(function () {
    avalues = [];
    addaValues();
    console.log(avalues);
    if (!validate(avalues)) {
      return;
    }
    let js_a = JSON.stringify(avalues);
    $.ajax({
      url: '/getallpassfilter',
      type: 'post',
      contentType: 'application/json',
      dataType: 'json',
      data: js_a,
      success: function () {

        updataAllpassFilterFrequencyResponse();
      }
    });
  });

  function addtolibrary() {
    if (!validate(avalues)) {
      return;
    }
    let js_a = JSON.stringify(avalues);
    $.ajax({
      url: '/updatelibrary',
      type: 'post',
      contentType: 'application/json',
      dataType: 'json',
      data: js_a,
      success: function () {
        flag = true;
        updatelibrary();
      }
    });


  }
  function addallpassfiltertodesign() {
    if (!validate(avalues)) {
      return;
    }
    temp = document.getElementById("a-values").value;
    allpassfilters.push(temp);
    let value = library[temp];
    let index = $('input[name="allpassfilters"]').length;
    $('#addFilterLoader').html('<i class="fas fa-check"></i>');

    $('#filters').append(`<div class="d-flex"><input type="checkbox" name="allpassfilters" id="${index}" value="${index}"/><label for="${index}">${value}</label></div>`);
    $(`#${index}`).change(function () {
      temp = ($(this).val());
      let index = allpassfilters[temp]
      let js_index = JSON.stringify(index);
      $.ajax({
        url: '/activateordeactivateallpassfilter',
        type: 'post',
        contentType: 'application/json',
        dataType: 'json',
        data: js_index,
        success: function (response) {
          allpassfilterszeros = response.allpassfilterzeros;
          allpassfilterspoles = response.allpassfilterpoles;
          updatefrequencyrespose();
        }
      });
    });
  }

  addfiltertolibrary.addEventListener("click", function () { addtolibrary(); });
  addfilter.addEventListener("click", function () { 
    addallpassfiltertodesign(); });


}());

