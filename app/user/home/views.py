from flask import Blueprint, render_template, g, flash, redirect, url_for, request
from app.functions import login_required
from app.services import config_srv
import json

bp = Blueprint("home", __name__, url_prefix="/home", template_folder="templates")
from .forms import ConfigForm


@bp.route("/")
@login_required()
def features():
    return render_template('feature.html')


@bp.route("data", methods=['post'])
@login_required()
def data():
    data_resource = []

    if request.form.get("default_field") is None:
        row = [
            request.form.get('event_code'),
            request.form.get('event_description'),
            request.form.get('argument_key'),
            request.form.get('argument_description'),
            request.form.get('type'),
            request.form.get("category"),
            request.form.get("principal"),
            request.form.get("remark"),
            request.form.get("pre_argument", None),
        ]
        data_resource.append(row)

    else:
        datas = config_srv.get_all()
        for data in datas:
            row = [
                request.form.get('event_code'),
                request.form.get('event_description'),
                data.argument_key,
                data.argument_description,
                data.type,
                request.form.get("category"),
                request.form.get("principal"),
                request.form.get("remark"),
                data.pre_argument
            ]
            data_resource.append(row)

    return json.dumps(data_resource)


@bp.route("config", methods=['get', 'post'])
@login_required()
def config():
    form = ConfigForm()

    if form.validate_on_submit():
        data = config_srv.get_first({"argument_key": form.data.get('argument_key'), "user_id": g.user.id})
        if data is None:
            config_srv.save(user_id=g.user.id, **form.data)

            flash("保存成功")
            return redirect(url_for(".config"))
        flash("参数key已经存在")

    datas = config_srv.get_all({"user_id": g.user.id})

    return render_template('config.html', form=form, configs=datas)


@bp.route("/delete/<int:_id>")
@login_required()
def delete(_id):
    if not config_srv.delete(_id, real=True):
        flash("删除失败")

    return redirect(url_for(".config"))
