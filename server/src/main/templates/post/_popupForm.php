<a class="b-close" >x</a>
<d class="message full">
  <form action="<?php echo url_for('post/submit'); ?>" method="post" id="post_new_popup_form"  enctype="multipart/form-data">
    <?php //echo $form; ?>

    <?php echo $form['_csrf_token']->render(array(
      'id' => 'post_csrf_token_popup'
    )); ?>
    <?php echo $form['user_id']->render(array(
      'id' => 'post_user_id_popup'
    )); ?>
    <?php echo $form['shared_post_id']->render(array(
      'id' => 'post_shared_post_id_popup'
    )); ?>
    <?php echo $form['body']->renderError() ?>
    <?php echo $form['body']->render(array(
      'placeholder' => __('post.placeholder', null, 'post'),
      'id'          => 'post_body_popup'
    )) ?>

    <div id="post_popup_form_uploads">
    <?php foreach ($form['new_attachements'] as $i=>$new_attachment_form):?>
      <?php echo $new_attachment_form['filename']->render(array('class'=>'post_selectfile select_file_'.$i)); ?>
      <?php echo $new_attachment_form['token']; ?>
      <?php echo $new_attachment_form['namespace']; ?>
      <?php echo $new_attachment_form['referer']; ?>
    <?php endforeach; ?>
    </div>

    <div id="post_new_popup_share_preview">
      Loading preview...
    </div>

    <input type="submit" value="Share" id="post_popup_submit_button">
  </form>
</d>