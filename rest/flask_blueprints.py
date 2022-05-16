import pprint

from flask import Blueprint, request

from singletons.app_singletons import companies_dao

bp = Blueprint('bp', __name__)


@bp.route('/params')
def params():
    sectors_and_industries = companies_dao.retrieve_sectors_and_industries()
    return {'MarketCapLowerThan(Optional)': 'Numeric',
            'MarketCapHigherThan(Optional)': 'Numeric',
            'OrderBy': ['PERatio', 'EVToEBITDA'],
            'Sector:[Industries]': sectors_and_industries}


@bp.route('/screener')
def screener():
    args = request.args.to_dict()
    if len(args) > 0 and (args['Sector'] or args['Industry']) and args['OrderBy']:
        return pprint.pformat([data for data in companies_dao.find_by(args)])

    return params()
