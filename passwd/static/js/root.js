$(document).ready(function() {
    var refresh_rate = 5000;

    var settings = $('#settings');
    var words = $('.words');
   
    function load_words() {
        
        $('.words div').fadeOut('slow', function() { $(this).remove() });

        $.getJSON(settings.attr('action'), $(settings).serialize(), function(data) {

            $.each(data.words, function(idx, val) {
                $(words[idx%words.length]).append('<div style="display:none">' + val + '</div>');            
            });
                       
            $('.words div').fadeIn('slow');

            window.setTimeout(load_words, refresh_rate);
        });
    }


    load_words();

});