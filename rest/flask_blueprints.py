from flask import Blueprint, request

from singletons.app_singletons import companies_dao

bp = Blueprint('bp', __name__)


@bp.route('/sectors')
def sectors():
    return companies_dao.retrieve_sectors().__str__()


@bp.route('/screener')
def screener():
    if len(request.args) > 0:
        return [data for data in companies_dao.find_by(request.args.to_dict())].__str__()

    return 'Please include "sector" and "metric" keys in your request'
