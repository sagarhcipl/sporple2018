import re
from elasticsearch_dsl import Search, Q, query
from main import elasticsearch


'''
Used for simple search / quick search only. For Search plus or advanced
search we use postgres because it provides more accurate results.
'''
def search_results(page, search_type, query_string, params={}):
    s = Search(index='users').using(elasticsearch)
    from_size = page * 10
    to_size = (page+1) * 10
    s = s[from_size:to_size]
    s = s.sort('_score',
        { 'doc.firstname': { 'order': 'asc' }},
        { 'doc.lastname': { 'order': 'asc' }})

    query_string = query_string.replace('/', '-')
    query_string = re.sub(r'[^\w\s-]+', '', query_string)
    sports = params.get('sports', 'rugby')
    terms = query_string.split(' ')
    special_terms = ['club', 'athlete', 'agent']
    plural_terms = [t+'s' for t in special_terms]
    profile_type = None

    for (i, term) in enumerate(terms):
        if term.lower() in plural_terms:
            profile_type = term[:-1].lower()
            terms.remove(term)
        elif term.lower() in special_terms:
            profile_type = term.lower()
            terms.remove(term)

    terms_string = ' '.join(terms)

    if sports and sports != 'all':
        q = Q('bool', must=[{'term': {'doc.sports': sports.lower()}}])
        s = s.query(q)

    q = Q('bool', must_not=[
            {'match': {'doc.avatar': 'empty_profile_image.png'}},
            {'match': {'doc.avatar': 'Clubs-default.png'}}
        ])
    s = s.query(q)

    if terms_string:
        query_string = terms_string + '*'
        q = Q('query_string', query=query_string,
            fields=[
                'doc.firstname^5',
                'doc.lastname^4',
                'doc.clubname^5',
                'doc.country^3',
                'doc.city^3',
                'doc.positions^2'])
        s = s.query(q)
        if profile_type:
            s = s.doc_type(profile_type)

    else:
        s = s.doc_type(profile_type)
    response = s.execute()
    return response


