/*
 * search js functions
 *
 */

var $searchToggle = undefined;
var $searchForm = undefined;
var $searchInput = undefined;
var $searchResCont = undefined;
var $searchResList = undefined;
var searchSport = undefined;
var lastQ = undefined;
var resultItemTmp = '<li class="search-results__list-item search-results__list-item--{{TYPE}} {{ISLAST}}">' +
                        '<a href="/profile/{{ID}}" class="search-results__profile-pic-cont {{PICCLASS}}">' +
                            '<img height="50" width="50" src="{{PIC}}" title="View {{NAME}}\'s Profile">' +
                        '</a>' +
                        '<div class="search-results__profile-details">' +
                            '<a href="/profile/{{ID}}" class="search-results__profile-name">' +
                                '{{NAME}}' +
                            '</a>' +
                            '<p class="search-results__profile-type">' +
                                '{{TYPE}} - {{COUNTRY}}' +
                            '</p>' +
                            '<p class="search-results__profile-additional">{{ADDITIONAL}}</p>' +
                        '</div>' +
                    '</li>';
var noResultTmp = '<li class="search-results__cta-item search-results__cta-item--no-results">' +
                        '<p>' +
                            'Sorry, no results' +
                        '</p>' +
                    '</li>';
var noMoreResultTmp = '<li class="search-results__cta-item search-results__cta-item--no-results">' +
                        '<p>' +
                            'Sorry, no more results' +
                        '</p>' +
                    '</li>';
var viewMoreResultTmp = '<li class="search-results__cta-item search-results__cta-item--more-results">' +
                        '<a href="/search/results?sport={{SPORT}}&searchTerms={{QUERY}}">' +
                            'View more results' +
                        '</a>' +
                    '</li>';

var _bind = function() {

    var searchTO = undefined;
    var searchDelay = 400;
    var minSearchLen = 3;
    var searchTransitionTime = 200;

    $searchInput.keyup(function(e){
        clearTimeout(searchTO);

        var q = $(this).val();
        //cache query
        lastQ = q;

        if (q.length >= minSearchLen){

            searchTO = setTimeout(function(){

                _fetch(q);

            }, searchDelay);
        
        }else{

            _showHideResults(false);
        }
    });

    //search form toggle for mobile and tablet
    $searchToggle.click(function(e) {
        e.preventDefault();

        var _$this = $(this);

        if( _$this.hasClass('active') ) {

            $searchForm.removeClass('open').height(0);
            _$this.removeClass('active');
            
        } else {

            var h = $searchInput.outerHeight(true).toFixed();

            _$this.addClass('active');
            $searchForm.height(h);

            setTimeout(function() {
                $searchForm.addClass('open');
            }, searchTransitionTime);
        }

    });

};

var _fetch = function(q) {

    $searchResList.html(''); 
    _showHideLoading(true);

    $.ajax({
        type: "POST",
        url: '/search',
        dataType: "json",
        data: {
            sport: searchSport,
            searchTerms: q
        },
        success: function(data) {

            var hitCount = data.total;
            var hits = data.hits.slice(0,5);

            _addResults(hits, hitCount);

        }
    });

};

var _showHideResults = function(show){

    if (show){

        //open
        $searchResCont.addClass('open');

        //bind close to clink anywhere but search
        config.jQEles.$bod.click(function(){
            _showHideResults();
        });

        $searchForm.click(function(e){
            e.stopPropagation(); 
        });

    } else {
        //remove close bing on body
        config.jQEles.$bod.off('click');
        $searchForm.off('click');

        //close
        $searchResCont.removeClass('open');
    }

}

var _showHideLoading = function(show){

    if (show){

        _showHideResults(true);

        $searchResCont.addClass('site-header__search-results-cont--loading');

    } else {

        $searchResCont.removeClass('site-header__search-results-cont--loading');
    }

}

var _addResults = function(hits, hitCount) {

    var resultsHTML = [];

    for (i in hits){
        var item = hits[i];
        var type = item._type;
        var profilePicClass = item._type === 'club' ? '' : 'profile-pic';
        var name = item._type === 'club' ? (item._source.doc.clubname || '') : ((item._source.doc.firstname || '') + ' ' + (item._source.doc.lastname || ''));
        var additional = (item._type === 'club' && item._source.doc.has_listings) ? 'Now Recruting' : (item._source.doc.positions || '');
        var isLast = (parseInt(i,10) + 1 === hits.length) ? 'search-results__list-item--last' : '';
        var filledItem = resultItemTmp
            .replace('{{ISLAST}}', isLast)
            .replace(/{{ID}}/g, item._id)
            .replace(/{{NAME}}/g, name)
            .replace('{{PIC}}', item._source.doc.avatar)
            .replace('{{PICCLASS}}', profilePicClass)
            .replace(/{{TYPE}}/g, type || '')
            .replace('{{COUNTRY}}', item._source.doc.country || '')
            .replace('{{ADDITIONAL}}', additional);

        resultsHTML.push(filledItem);
    }

    //add list footer
    if (!hits.length){

        resultsHTML.push(noResultTmp);

    } else if (hitCount > hits.length){
        //TODO: why isnt this condition firing
        
        var filledViewMoreResult = viewMoreResultTmp
            .replace('{{SPORT}}', searchSport)
            .replace('{{QUERY}}', lastQ);

        resultsHTML.push(filledViewMoreResult);
    } else {

        //resultsHTML.push(noMoreResultTmp);

        var filledViewMoreResult = viewMoreResultTmp
            .replace('{{SPORT}}', searchSport)
            .replace('{{QUERY}}', lastQ);

        resultsHTML.push(filledViewMoreResult);
    }

    //hide loading
    _showHideLoading(false);

    //clear prev results & append results
    $searchResList.html(resultsHTML.join(''));    

};

var setup = function() {
    
    $searchToggle = $('#nav-itm--search');
    $searchForm = $('#search-form');
    $searchInput = $('#site-header__search-box');
    $searchResCont = $('#site-header__search-results-cont');
    $searchResList = $('#site-header__search-results');
    searchSport = $searchForm.children('input[name="sport"]').val();

    if($searchInput.length) {

        _bind();

    }

};

module.exports = {
    setup: setup
};
