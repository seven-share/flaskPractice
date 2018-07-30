from app.model.models import Product,Product_Image,Product_Property
def getRecentProducts(count):
    recentProducts=Product.query.order_by(Product.create_time.desc()).limit(count).all()
    return [rp.to_json() for rp in recentProducts]
def getProductsByCategoryID(id):
    ProductsByCategoryID=Product.query.filter_by(category_id=id).all()
    return [pc.to_json() for pc in ProductsByCategoryID]
def getProductDetail(id):
    product=Product.query.get(id)
    product_images=product.product_image.order_by(Product_Image.order.asc()).all()
    product_images=[pi.to_json() for pi in product_images]
    product_propertys=product.product_property.all()
    product_propertys=[pp.to_json() for pp in product_propertys]
    product=product.to_json()
    product['product_images']=product_images
    product['product_propertys']=product_propertys
    return product