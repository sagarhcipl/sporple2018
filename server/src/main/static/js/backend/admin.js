$(document).ready(function () {
    $('#batch_submit_button').click(function (e) {
        e.preventDefault();

        $form = $(this).parents('form:first');
        copyIds();

        if ($('select[name="batch_action"]').val() === 'batchDelete') {
            $nbUsers = $('.sf_admin_batch_checkbox:checked').length;

            bootbox.confirm(
                'You are about to delete <b>' + $nbUsers + '</b> users. Are you sure ?',
                'No',
                'Yes',
                function (result) {
                    if (result) {
                        $form.submit();
                    }
                }
            );
        } else {
            $form.submit();
        }
    });
});

