    $(document).ready(function () {
    $('#addfriend').click(function () {
        var profile_owner_id = $(this).data("pk");
        $.post('profile/'+profile_owner_id+'/friend_request_sent/', function (data) {
            $('#addfriend').fadeOut();
        });
    });
    $('#cancelfriend').click(function () {
        var profile_owner_id = $(this).data("pk");
        $.get('profile/'+profile_owner_id+'/friend_request_cancelled/', function (data) {
            $('#cancelfriend').fadeOut();
        });
    });
})