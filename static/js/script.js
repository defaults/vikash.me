function resend(){
    $.ajax({
      url: "/write/resend_mail",
    })
    .done(function() {
        $('#status').html('Mail send to your admin email id.');
    });
}
