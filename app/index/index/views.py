from flask import Blueprint, flash, redirect, render_template, request, session

from app.functions import login_required, url_for

bp = Blueprint("index", __name__, url_prefix="", template_folder="templates")


@bp.route('/')
def index():
    return render_template('index.html')
