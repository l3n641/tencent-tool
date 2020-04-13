from flask import Blueprint, render_template, g, flash, redirect, url_for, request, current_app
from app.functions import login_required
from app.services import config_srv
import json, os
from app.constants import EXCEL_EXTENSIONS
from app.functions import allowed_file
import pandas

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
        data_resource = get_datas(**request.form)

    return json.dumps(data_resource)


@bp.route("config", methods=['get', 'post'])
@login_required()
def config():
    config_type = request.args.get("config_type", 0)
    form = ConfigForm()
    form.config_type_id.data = config_type
    if form.validate_on_submit():
        data = config_srv.get_first(
            {"argument_key": form.data.get('argument_key'), "config_type_id": config_type, "user_id": g.user.id})
        if data is None:
            config_srv.save(user_id=g.user.id, **form.data)

            flash("保存成功")
            return redirect(url_for(".config", config_type=config_type))
        flash("参数key已经存在")

    datas = config_srv.get_all({"user_id": g.user.id, "config_type_id": config_type})

    return render_template('config.html', form=form, configs=datas)


@bp.route("/delete/<int:_id>")
@login_required()
def delete(_id):
    if not config_srv.delete(_id, real=True):
        flash("删除失败")

    return redirect(url_for(".config"))


@bp.route("/upload", methods=['POST'])
@login_required()
def upload():
    """文件上传"""

    file = request.files.get("Filedata")

    upload_path = os.path.join(current_app.static_folder, 'upload')

    if not os.path.exists(upload_path):
        os.makedirs(upload_path)

    # 如果上传的是文档格式 后缀
    if file and allowed_file(file.filename, EXCEL_EXTENSIONS):

        file_name = file.filename
        file_path = os.path.join(upload_path, file_name)
        file.save(file_path)
        frame = pandas.read_excel(file_path)
        data_resource = []
        frame = frame.fillna("")
        for index, row in frame.iterrows():
            event_code = row.get("事件code")
            event_description = row.get("事件说明")
            category = row.get("分类")
            principal = row.get("负责人")
            remark = row.get("备注")
            sub_datas = get_datas(event_code=event_code, event_description=event_description, category=category,
                                  principal=principal, remark=remark)
            data_resource.extend(sub_datas)

        os.remove(file_path)
        return json.dumps(data_resource)

    return json.dumps({
    })


def get_datas(event_code, event_description, category, principal, remark, **kwargs):
    data_resource = []

    datas = config_srv.get_all({"user_id": g.user.id})
    for data in datas:
        row = [
            event_code,
            event_description,
            data.argument_key,
            data.argument_description,
            data.type,
            category,
            principal,
            remark,
            data.pre_argument
        ]
        data_resource.append(row)

    return data_resource
