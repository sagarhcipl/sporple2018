import db
import math
import util
from flask import abort
from flask import jsonify
from flask import render_template
from flask import request
from flask import url_for
from flask.ext.login import current_user
from flask.ext.login import login_required
from forms import query_selectors
from forms.advanced_search import AdvancedSearchForm
from forms.search_opportunity import SearchOpportunity
from search import elasticsearch
from search import controller
from payment import controller as pcontroller

# Quick search
@login_required
def main():
    query_string = request.values.get('searchTerms')
    params = util.request_to_dict(request.values)
    results = elasticsearch.search_results(
            page=0,
            search_type='simple',
            query_string=query_string,
            params=params)
    return jsonify(results.to_dict().get('hits', {}))


'''
Depending on request type, the view will either call
search controller that performs a query on postgres or will call
elasticsearch that perform simple quick search. The result page
is also rendered accordingly.
'''
@login_required
def result_page(page=0, request_type='simple'):
    page = int(page)
    query_string = request.values.get('searchTerms')
    params = util.request_to_dict(request.values)
    search_type = request.values.get('searchType', request_type)
    if search_type == 'simple' and not query_string:
        return ''
    if search_type != 'simple':
        results, total = controller.search_advanced(page, params)
        total_pages = int(math.ceil(total / 10.0))
        params['page'] = '-page-'
        results_url = url_for('search.results', **params)
        return render_template('search/advanced_results.html',
            search_type=search_type, results=results,
            total_pages=total_pages, current_page=page, total=total,
            results_url=results_url)
    else:
        results = elasticsearch.search_results(
            page, search_type, query_string, params)
        total = results.hits.total
        total_pages = int(math.ceil(total / 10.0))
        params['page'] = '-page-'
        results_url = url_for('search.results', **params)

        return render_template('search/results.html',
            search_type=search_type, results=results,
            total_pages=total_pages, current_page=page,
            results_url=results_url)


@login_required
def advanced():
    _is_allowed = pcontroller.pro_plan(current_user.user)
    if not _is_allowed:
        return render_template('plan/go_to_premium.html')
    if request.method == 'POST':
        return result_page(request_type='advanced')
    form = AdvancedSearchForm(sports=current_user.user.sport)
    all_sports = db.Sport.query.all()
    return render_template('forms/advanced_search.html', form=form, all_sports=all_sports)


@login_required
def opportunities():
    profile = current_user.user.profile
    if not profile.user.sport:
        abort(403)
    form = SearchOpportunity()
    form.positions.query = query_selectors.user_position_list(profile.user.sport.id, blank=True)
    form.country.query = query_selectors.country_list(blank=True)

    if request.method == 'GET':
        position_ids = request.args.getlist('positions')
        positions = []
        if position_ids:
            form.positions.data = db.Position.query.filter(db.Position.id.in_(position_ids)).all()
        country_ids = request.args.getlist('country')
        if country_ids:
            form.country.data = db.Country.query.filter(db.Country.id.in_(country_ids)).all()

    page = int(request.values.get('page', 0))

    listings, total = controller.search_opportunity(form, page)
    total_pages = int(math.ceil(total / 10.0))
    params = util.request_to_dict(request.values)
    params['page'] = '-page-'
    results_url = url_for('opportunities', **params)
    return render_template('forms/search_opportunity.html', form=form,
            listings=listings, total_pages=total_pages, current_page=page,
            results_url=results_url)

