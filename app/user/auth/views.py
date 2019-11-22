# -*- coding: utf-8 -*-

from flask import Blueprint, flash, redirect, render_template, request, session

from app.functions import login_required, url_for
from app.services import user_srv
from .forms import LoginForm

bp = Blueprint("auth", __name__, url_prefix="/auth", template_folder="templates")


@bp.route("/login", methods=['GET', 'POST'])
def login():
    """登录"""

    if "user_id" in session:
        return redirect(request.args.get("next") or url_for("home.features"))

    form = LoginForm()
    if form.validate_on_submit():
        user = user_srv.get_by_account(form.account.data)
        if user and user.verify_password(form.password.data):
            session["user_id"] = user.id
            return redirect(url_for(request.args.get("next") or "home.features"))
        flash("登录失败")


    return render_template("login.html", form=form)


@bp.route("/logout")
@login_required()
def logout():
    """登出"""

    session.clear()

    return redirect(url_for(".login", next=request.args.get("next")))
