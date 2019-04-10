/*
 * search js functions
 *
 */

var $searchForm = undefined;
var $searchInput = undefined;
var $searchResCont = undefined;
var $searchResList = undefined;
var searchSport = undefined;
var lastQ = undefined;
var addNewEnabled = false;
var resultItemTmp = '<li class="search-results__list-item search-results__list-item--{{TYPE}} {{ISLAST}}" data-user-id="{{ID}}">' +
                        '<a data-user-id="{{ID}}" class="search-results__profile-pic-cont {{PICCLASS}}">' +
                            '<img src="{{PIC}}" title="View {{NAME}}\'s Profile">' +
                        '</a>' +
                        '<div class="search-results__profile-details">' +
                            '<a data-user-id="{{ID}}" class="search-results__profile-name">' +
                                '{{NAME}}' +
                            '</a>' +
                            '<p class="search-results__profile-type">' +
                                '{{TYPE}} - {{COUNTRY}}' +
                            '</p>' +
                            '<p class="search-results__profile-additional">{{ADDITIONAL}}</p>' +
                        '</div>' +
                    '</li>';
var noResultsFound = '<li class="search-results-no-items">' +
                        '<p>Could not find any match</p>' +
                     '</li>';
var addNewUser = '<li class="search-results-add-new"><a><i class="fa fa-plus"></i> Add User {{NAME}}</a></li>';

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
        $searchResCont.removeClass('hidden');

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
        $searchResCont.addClass('hidden');
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
        var additional = (item._type === 'club' && item._source.doc.has_listings) ? 'Now Recruting' : '';
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

    if (addNewEnabled) {
        var newUserHtml = addNewUser.replace('{{NAME}}', $searchInput.val());
        resultsHTML.push(addNewUser);
    }

    //hide loading
    _showHideLoading(false);

    //clear prev results & append results
    $searchResList.html(resultsHTML.join(''));    

};

var setup = function(searchFormId, searchResultContId, showAddNew) {
    $searchForm = $('#' + searchFormId);
    $searchInput = $searchForm.find('input[type=text]');
    $searchResCont = $('#' + searchResultContId);
    searchSport = $searchForm.find('input[name="sport"]').val();
    addNewEnabled = showAddNew;

    if($searchResCont.length) {
        var searchResListId = searchResultContId + '-list';
        $searchResCont.append('<ul id="' + searchResListId + '" class="quick-search-results"></ul>');
        $searchResList = $('#' + searchResListId);
    }

    if($searchInput.length) {
        _bind();
    }
};

module.exports = {
    setup: setup
};
