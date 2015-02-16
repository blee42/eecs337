(function() {
    $('.winners-content').click(function(event) {
        $($(event.target).next()).toggle(200);
    });
    $('.winners-content h3').click(function(event) {
        event.stopPropagation();
        $($(event.target).parent().next()).toggle(200);
    });
    $('.winners-content h4').click(function(event) {
        event.stopPropagation();
        $($(event.target).parent().next()).toggle(200);
    });
}).call(this);
