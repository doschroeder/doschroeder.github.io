// Turn cloaked e-mail addresses into clickable mailto links
document.addEventListener('DOMContentLoaded', function () {
  var emailSpans = document.getElementsByClassName('cloaked-e-mail');
  for (var i = 0; i < emailSpans.length; i++) {
    var span = emailSpans[i];
    var user = span.getAttribute('data-user').split('').reverse().join('');
    var domain = span.getAttribute('data-domain').split('').reverse().join('');
    var link = document.createElement('a');
    link.href = 'mailto:' + user + '@' + domain;
    link.innerText = user + '@' + domain;
    span.parentElement.insertBefore(link, span);
    span.parentElement.removeChild(span);
  }
});
