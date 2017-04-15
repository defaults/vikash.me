(function () {
    var preElements = document.getElementsByTagName('pre');
    for(var i = 0; i < preElements.length; i++) {
        preElements[i].classList.add('prettyprint');
    }
})();

function resend(){
    $.ajax({
      url: "/write/resend_mail",
    })
    .done(function() {
        $('#status').html('Mail send to your admin email id.');
    });
}
