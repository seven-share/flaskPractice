from app.model.models import Theme
from app.validation import isNotFind
from flask import  current_app

def getThemeList(ls):
    results=[]
    for l in ls:
        result=Theme.query.get(l)
        isNotFind('/theme',result)
        result=result.to_json()
        results.append(result)
    return results

def getThemeDetial(id):
    theme=Theme.query.get(id)
    isNotFind('/theme',theme)
    products=theme.productInTheme.all()
    backProducts = []
    for pt in products:
        backProduct=pt.backProduct
        bp={
            'id':backProduct.id,
            'name':backProduct.name,
            'price':str(backProduct.price),
            'stock':backProduct.stock,
            'category_id':backProduct.category_id,
            'main_img_url':current_app.config.get('IMG_PREFIX')+backProduct.main_img_url,
            'come_from':backProduct.come_from
        }
        backProducts.append(bp)
    themeDetail={
        'id': theme.id,
        'name': theme.name,
        'description': theme.description,
        'topic_img': theme.topic_img.totalUrl(),
        'head_img': theme.head_img.totalUrl(),
        'productInTheme': backProducts
    }



    return themeDetail