function newsletter_check_field(field,message){if(!field)return!0;if(field.type=="checkbox"&&!field.checked){alert(message);return!1}
if(field.required!==undefined&&field.required!==!1&&field.value==""){alert(message);return!1}
return!0}
function newsletter_check(f){var re=/^([a-zA-Z0-9_\.\-\+])+\@(([a-zA-Z0-9\-]{1,})+\.)+([a-zA-Z0-9]{2,})+$/;if(!re.test(f.elements.ne.value)){alert(newsletter.messages.email_error);return!1}
if(!newsletter_check_field(f.elements.nn,newsletter.messages.name_error))return!1;if(!newsletter_check_field(f.elements.ns,newsletter.messages.surname_error))return!1;for(var i=1;i<newsletter.profile_max;i++){if(!newsletter_check_field(f.elements["np"+i],newsletter.messages.profile_error))return!1}
if(!newsletter_check_field(f.elements.ny,newsletter.messages.privacy_error))return!1;return!0}