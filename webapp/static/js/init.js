tag_data = {
  'precondition': null,
  'solution': null,
  'both': null,
  'other': null
};

tag_data = {
  'P': null,
  'S': null,
  'B': null,
  'O': null
};


document.addEventListener('DOMContentLoaded', function() {
  var elems = document.querySelectorAll('.chips');
  var instances = M.Chips.init(elems, options);
});

// Or with jQuery

$('.chips').chips();

$('.chips-placeholder').chips({
  placeholder: '+tag',
  secondaryPlaceholder: '+tag',
});
$('.chips-autocomplete').chips({
  autocompleteOptions: {
    data: tag_data,
    limit: 1,
    minLength: 1
  }
});

document.addEventListener('DOMContentLoaded', function() {
  var elems = document.querySelectorAll('.autocomplete');
  var instances = M.Autocomplete.init(elems, options);
});


// Or with jQuery

$(document).ready(function(){
  $('input.autocomplete').autocomplete({
    data: tag_data,
  });
});

document.addEventListener('DOMContentLoaded', function() {
  var elems = document.querySelectorAll('.collapsible');
  var instances = M.Collapsible.init(elems, options);
});

// Or with jQuery

$(document).ready(function(){
  $('.collapsible').collapsible();
});

document.addEventListener('DOMContentLoaded', function() {
  var elems = document.querySelectorAll('select');
  var instances = M.FormSelect.init(elems, options);
});

// Or with jQuery

$(document).ready(function(){
  $('select').formSelect();
});