$(document).ready(function () {
    var $inviteFriendContainer = $('div.invite-a-friend-container');

    $inviteFriendContainer.on('click', 'a.invite-again', function (e) {
        e.preventDefault();

        $.get($(this).attr('href'), function (data) {
            $inviteFriendContainer.html(data);
        });
    });

    $inviteFriendContainer.on('submit', '#invite-a-friend', function (e) {
        e.preventDefault();

        $.ajax({
            type: "POST",
            url: $(this).attr('action'),
            data: $(this).serialize(),
            success: function (data) {
                if (data.error) {
                    alert(data.error);
                } else {
                    $('div.invite-a-friend-container').html(data);
                }
            }
        });
    });
});
