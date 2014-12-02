$(function() {
    var cache = {};
    $( "#replyto" ).autocomplete({
      minLength: 2,
      source: function( request, response ) {
        var term = request.term;
 
        $.getJSON( "getMatchingEmailWS", { match: request.term, type: 'json' }, function( data ) {
            response( $.map( data, function( item ) {
              return {
                label: item.f + " " + item.m + " " + item.l + " <" + item.e + ">",
                value: item.e
              }
            }));
        });
      }
    });
  });
