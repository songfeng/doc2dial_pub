tag_data = {"verse_missing_emails": null, "slm_troubleshoot": null, "ecprint_troubleshooting": null, "devices_at_worksystem": null, "hw_support": null, "getting_started_mac_worksystem": null, "mac_windows_vm": null, "mail_id_support": null, "att_errors": null, "webex_meetings": null}

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