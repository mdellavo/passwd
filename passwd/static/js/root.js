$(document).ready(function() {
    var refresh_rate = 5000;

    var settings = $('#settings');
    var words = $('.words');

    var timer = null;

    function set_timeout() {
        if(!timer)
            timer = window.setTimeout(load_words, refresh_rate);        
    }

    function clear_timeout() {
        if(timer) {
            window.clearTimeout(timer);
            timer = null;  
        }         
    }
    
    function load_words() {
        
        $('.words div').fadeOut('slow', function() { $(this).remove() });

        $.getJSON(
            settings.attr('action'), 
            settings.serialize(), 
            function(data) {              
                $.each(
                    data.words, 
                    function(idx, val) {
                        var msg = '<div class="word" style="display:none">' + val + '</div>';
                        $(words[idx%words.length]).append(msg);        
                    });
            
            $('.words div').fadeIn('slow');

            if($('#auto-refresh').attr('checked')) 
                set_timeout();
        });
    }

    load_words();

    $('#auto-refresh').change(function() {
        if(this.checked) {
            $('#refresh-now').attr('disabled', 'disabled')
            set_timeout();
        } else {
            $('#refresh-now').attr('disabled', null)
            clear_timeout();
        }
    }).change();

    $('#words-container').hover(
        function() { 
            if($('#auto-refresh').attr('checked')) {
                $('#paused').fadeIn('fast');
                clear_timeout();
            }
        }, 
        function() { 
            if($('#auto-refresh').attr('checked')) {
                $('#paused').fadeOut('fast');
                if($('#auto-refresh').attr('checked')) 
                    set_timeout();
            }
        } 
    );

    function update_url() {
        var url = window.location.origin + settings.attr('action') + '?' + 
            settings.serialize();
        $('#url').html(url).attr('href', url);
    }

    settings.find(':input').change(update_url);
    update_url();

    $('#refresh-now').click(function() {
        load_words();
        return false;
    });

    $('.word').live({
        mouseenter: function() {
            $(this).addClass('glow');
        },
        mouseleave: function() {
            $(this).removeClass('glow');            
        }
    });
});
