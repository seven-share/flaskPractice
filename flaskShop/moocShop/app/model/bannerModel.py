from app.model.models import Banner
from app.validation import isNotFind

def getBannerByid(id):
        banner=Banner.query.get(id)
        isNotFind('/banner/<id>',banner)
        banner_items=banner.banner_items
        return [banner_item.to_json() for banner_item in banner_items]