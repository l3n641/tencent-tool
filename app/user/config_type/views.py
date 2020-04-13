from flask import Blueprint, render_template, request, g, flash, redirect, url_for, abort
from app.functions import login_required
from app.services import config_type_srv
from app.constants import DEFAULT_PAGE
from .forms import ConfigTypeForm

bp = Blueprint('config_type', __name__, url_prefix="/config_type", template_folder="templates")


@bp.route("/")
@login_required()
def index():
    page = int(request.args.get('page') or DEFAULT_PAGE)
    datas = config_type_srv.get_list(where={"user_id": g.user.id}, page=page)
    return render_template('index.html', datas=datas)


@bp.route('edit', methods=['get', 'post'])
@bp.route('edit/<int:_id>', methods=['get', 'post'])
@login_required()
def edit(_id=None):
    if _id:
        data = config_type_srv.get_first({"id": _id, "user_id": g.user.id})
        if data is None:
            abort(404)
        form = ConfigTypeForm(obj=data)
    else:
        form = ConfigTypeForm()

    if form.validate_on_submit():
        config_type_srv.save(id=_id, user_id=g.user.id, **form.data)
        flash("保存成功")
        return redirect(url_for(".index"))

    return render_template('edit.html', form=form)


@bp.route("delete/<int:_id>")
@login_required()
def delete(_id):
    data = config_type_srv.get_first({"id": _id, "user_id": g.user.id})
    if data is None:
        abort(404)
    config_type_srv.delete_with_config_data(_id)
    flash("删除成功")
    return redirect(url_for(".index"))
