// JQuery
console.log('JS ready!!!')
$( document ).ready(function() {
    $( ".like_unlike_btn" ).click(function( event ) {

        // Button id should contain like pointer, target pointer & target id
        // ex: question_like_{id}
        event.preventDefault();

        const id_tag_array = $(this).attr('id').split('_');
        const target = id_tag_array[0].trim();
        const choice = id_tag_array[1].trim();
        const reversed_choice = (choice === 'like') ? 'unlike' : 'like';
        const id = id_tag_array[2].trim();
        const url = $(this).attr('href');
        let current_btn = $(this);
        let reversed_btn = $(`#${target}_${reversed_choice}_${id}`)

        $.ajax({
            type: 'POST',
            url: url,
            data: {
                'csrfmiddlewaretoken': csrf_token,
                'id': id,
                'target': target,
                'choice': choice,
            },
            success: function(response) {
                $(`#${target}_${choice}_count_${id}`).text(response.cnt);
                $(`#${target}_${reversed_choice}_count_${id}`).text(response.reversed_cnt);
                if (response.status === 'checked'){
                    current_btn.removeClass('text-primary');
                    current_btn.addClass('text-danger');
                }
                else {
                    current_btn.removeClass('text-danger');
                    current_btn.addClass('text-primary');
                }
                if (response.reversed_status === 'checked'){
                    reversed_btn.removeClass('text-primary');
                    reversed_btn.addClass('text-danger');
                }
                else {
                    reversed_btn.removeClass('text-danger');
                    reversed_btn.addClass('text-primary');
                }
            },
            error: function(response) {
                console.log('error');

            }
        })
    });
});