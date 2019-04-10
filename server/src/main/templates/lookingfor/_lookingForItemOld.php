<li>
<div class="player_query">
  <div class="Holder">
    <span class="agent_agency">
	<?php use_helper('Inflector');?>

	<?php echo ooip_thumb_tag($profile->getAgencyImage(), 'alt_title=Profile image size=59x59 scale=1 inflate=1 quality=100'); ?>
    </span>
    <span class="agent_title">
      <?php echo $looking_for->getTitle();?></span>
  </div>
  <div class="textHolder">
    <em>Sport</em>
    <strong><?php echo __(SportCache::getSlugById($looking_for->getSportId()),null, 'sport');?></strong>
    <em>Position</em>
    <strong><?php echo $looking_for->getTitle();?></strong>
    <em>Country</em>
    <strong><?php echo $looking_for->getCountry();?></strong>
  </div>
  <div class="verticaldivider"></div>
  <div class="textBox">
    <p><span class="textBoxTrim"><?php echo $looking_for->getBody();?></span>
      <a href="#" class="looking_for_more" data-target="#looking_for_view_<?php echo $looking_for->getId(); ?>">more...</a>
    </p>

    <div class="textBoxHide" id="looking_for_view_<?php echo $looking_for->getId(); ?>" data-user-id="<?php echo $user_id; ?>">
      <h2 class="ttl ttl--lower modal__user-badge">
        <span class="profile-pic"><?php echo ooip_thumb_tag($profile->getImage(), 'alt_title=Profile image size=30x30 scale=1 inflate=1 quality=90'); ?></span>
        <?php echo user_name($user_id); ?>
      </h2>
    	<p><?php echo $looking_for->getBody();?></p>
    	<h3 class="ttl3">Message me if you are interested.</h3>
    </div>
    
    <a href="#" class="view" data-target="#looking_for_view_<?php echo $looking_for->getId(); ?>">View</a>
  </div>
</div>
</li>
