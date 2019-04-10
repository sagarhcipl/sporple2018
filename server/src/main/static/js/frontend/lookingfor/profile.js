var lookingFor = {
    init: function (){
    	this.cutNames();
    	this.placeholderName();
     	this.textBoxTrim();
    },

  	cutNames: function() {
      return false; // not needed? -
      // generates a bug on the "Endorsements" of an agents profile - removing endorsement names
    	  $('.name').each(function () {
    	       $(this).text(
    	         $(this)
    	           .text()
    	           .split(' ')[0]
    	         );
    	  });
  	},

  	placeholderName: function () {
  		if($('.player_query_placeholder').length == 1) {
  			$('.player_query_name').text($('.player_name').text());
  		}
  	},

  	textBoxTrim: function () {
  	$('.textBoxTrim').each(function () {
  	     $(this).text(
  	     	$(this)
  	     		.text()
  	     		.substr(0,150)
  	     		.trim()
  	     );
  		});
  	}
}

$(document).ready(function () {
    lookingFor.init();
});
