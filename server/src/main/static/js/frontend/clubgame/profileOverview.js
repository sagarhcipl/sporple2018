var clubGameProfileOverviewController = new function() {

  var self;

  this.user_id = false;
  this.league_id = false;
  this.team_id = false;

  this.init = function() {
    self = this;

    this.user_id = cg_user_id;

    $('#game_added_confirmation_container_no_button').click(function(e) {
      e.preventDefault();
      $('#game_added_confirmation_container').hide();
      $('#cg_interface').html('');
    });

    $('#game_added_confirmation_container_yes_button').click(function(e) {
      e.preventDefault();
      $('#game_added_confirmation_container').hide();
    });

    this.bindEvents();
  }

  /// league form

  this.reloadProfileOverviewBase = function() {
    $('#cg_profile_team_id_container').html('');
    $('#cg_profile_league_id_container').load(cg_profile_league_selector_url + '?user_id=' + self.user_id, function () {
      self.bindEvents();
    });
  }


  this.bindEvents = function() {

    $('#cg_profile_league_id_select').change(function() {
      $.post($("#cg_profile_league_form").attr('action'), $("#cg_profile_league_form").serialize(), function(data) {
        $('#cg_profile_team_id_container').html(data);

        $('#cg_league_team_team_select').change(function() {
          $.post($("#cg_profile_team_form").attr('action'), $("#cg_profile_team_form").serialize(), function(data) {
            $('#cg_list_content').html(data);
            $('#cg_interface').html('');

            self.bindEventsForList();

          });
        });

      });
    });

    $('#cg_add_league_button').click(function(e) {
      e.preventDefault();
      $('#cg_interface').load(cg_league_form_url, function () {
        self.bindEventsForLeagueForm();
      });
    });

  }

  this.bindEventsForList = function() {
    // add games button
    $('#cg_profile_overview_add_games_button').click(function(e) {
      e.preventDefault();
      $('#cg_interface').load($(this).attr('href'), function () {
        self.bindEventsForGameForm();
      });
    });

    // delete game buttons
    $('.cg_game_delete_button').click(function(e) {
      e.preventDefault();
      $('#cg_list_content').load($(this).attr('href'), function() {
        self.bindEventsForList();
      });
    });

    // back button (close list)
    $('.cg_game_list_back_button').click(function(e) {
      $('#cg_list_content').html('');
    });
  }

  // -=--=-=-=--=-==-----------


  this.bindEventsForLeagueForm = function() {

    $('.cg_league_form_cancel_button').click(function(e) {
      e.preventDefault();
      $('#cg_interface').html('');
    });

    $('#cg_league_input_submit_button').click(function() {
      $('#cg_team_name_input').attr('value', '');
      $('#cg_league_id_delete').attr('value', '');
      $('#cg_team_id_delete').attr('value', '');
      self.submitLeagueForm();
    });
    $('#cg_team_input_submit_button').click(function() {
      $('#cg_league_name_input').attr('value', '');
      $('#cg_league_id_delete').attr('value', '');
      $('#cg_team_id_delete').attr('value', '');
      self.submitLeagueForm();
    });
    $('#cg_league_team_league_select').change(function() {
      $('#cg_league_name_input').attr('value', '');
      $('#cg_team_name_input').attr('value', '');
      $('#cg_league_id_delete').attr('value', '');
      $('#cg_team_id_delete').attr('value', '');
      self.submitLeagueForm();
    });

    $('.cg_league_delete').click(function (e) {
      e.preventDefault();
      var league_id = $(this).attr('data-league-id');
      $('#cg_league_name_input').attr('value', '');
      $('#cg_team_name_input').attr('value', '');
      $('#cg_team_id_delete').attr('value', '');

      $('#cg_league_id_delete').attr('value', league_id);
      self.submitLeagueForm();
    });
    $('.cg_team_delete').click(function (e) {
      e.preventDefault();
      var team_id = $(this).attr('data-team-id');
      $('#cg_league_name_input').attr('value', '');
      $('#cg_team_name_input').attr('value', '');
      $('#cg_league_id_delete').attr('value', '');

      $('#cg_team_id_delete').attr('value', team_id);
      self.submitLeagueForm();
    });


    $('#cg_league_form').submit(function (e) {
      e.preventDefault();
    });

  }

  this.submitLeagueForm = function() {
    $.post($("#cg_league_form").attr('action'), $("#cg_league_form").serialize(), function(data) {
      $('#cg_interface').html(data);
      self.reloadProfileOverviewBase();
      self.bindEventsForLeagueForm();
    });
  }



  /// game form

  this.bindEventsForGameForm = function() {
    $('.cg_game_form_cancel_button').click(function (e) {
      e.preventDefault();
      $('#cg_interface').html('');
    });

    $('#cg_game_form').submit(function (e) {
      e.preventDefault();
      self.submitGameForm();
    });
  }

  this.submitGameForm = function() {
    self.team_id = $('select#cg_game_team_select option:selected').val();
    $.post($("#cg_game_form").attr('action'), $("#cg_game_form").serialize(), function(data) {
      $('#cg_interface').html(data);
      self.bindEventsForGameForm();

      // redraw games list
      // cg_profile_team_change_url
      $('#cg_list_content').load(cg_profile_team_change_url + "?team_id=" + self.team_id, function() {
        self.bindEventsForList();
      });

      // show confirmation + ask to add another
      $('#game_added_confirmation_container').show();


    });
  }






}





$(function() {

  clubGameProfileOverviewController.init();

});