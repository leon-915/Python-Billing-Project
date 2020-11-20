"""Plan resource for handling any plan requests"""
from flask import request, render_template, make_response
from datetime import datetime as dt
from flask import current_app as app
from src.models.plans import Subscription, db, Plan

class Plan(Resource):
    """Resource/routes for subscription endpoints"""

    def get(self, sid):
        """External facing subscription endpoint GET

        Gets an existing Subscription object by id

        Args:
            sid (int): id of subscription object

        Returns:
            json: serialized subscription object

        """
        subscription = get_object_or_404(Subscription, sid)
        result = SubscriptionSchema().dump(subscription)
        return jsonify(result.data)