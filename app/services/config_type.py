from .common import CommonService


class ConfigTypeService(CommonService):
    def delete_with_config_data(_self, id):
        from app.services import config_srv
        config_srv.delete({"config_type_id": id}, real=True)
        return super().delete({"id": id}, real=True)
