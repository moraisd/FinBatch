import pprint

from flask import Blueprint, request

from singletons.app_singletons import companies_dao

bp = Blueprint('bp', __name__)


@bp.route('/params')
def params():
    return {'Sector': (companies_dao.retrieve_sectors()),
            'MarketCapLowerThan': 'Numeric',
            'MarketCapHigherThan': 'Numeric',
            'OrderBy': ['PERatio', 'EVToEBITDA']}


@bp.route('/screener', methods=['POST'])
def screener():
    if len(request.form) > 0:
        args = request.form.to_dict()

        return pprint.pformat([data for data in companies_dao.find_by(args)])

    return params()
