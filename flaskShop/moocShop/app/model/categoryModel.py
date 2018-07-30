from app.model.models import Category
from app.validation import isNotFind
def getAllCategory():
    category = Category.query.all()
    isNotFind('/category/all', category)
    return [cg.to_json() for cg in category]