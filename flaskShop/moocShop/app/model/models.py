from app import db
from datetime import datetime
from flask import current_app
import json

class Banner(db.Model):
    __tablename__ = 'banner'
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String)
    description=db.Column(db.String)
    delete_time=db.Column(db.DateTime,default=datetime.now())
    update_time=db.Column(db.DateTime,default=datetime.now())
    banner_items=db.relationship('Banner_item',backref='banner',lazy='dynamic')

class Banner_item(db.Model):
    __tablename__ = 'banner_item'
    id = db.Column(db.Integer, primary_key=True)
    img_id=db.Column(db.Integer,db.ForeignKey('image.id'))
    img=db.relationship('Image',backref='banner_item',uselist=False)
    key_word=db.Column(db.String)
    type=db.Column(db.Integer)
    banner_id=db.Column(db.Integer,db.ForeignKey('banner.id'))
    delete_time=db.Column(db.DateTime,default=datetime.now())
    update_time=db.Column(db.DateTime,default=datetime.now())
    def to_json(self):
        if self.img.come_from==1:
            json_banner_item={
                'img':self.img.totalUrl(),
                'key_word':self.key_word,
                'type':self.type
            }
        else:
            json_banner_item={
                'img':self.img.url,
                'key_word':self.key_word,
                'type':self.type
            }
        return json_banner_item
class Image(db.Model):
    __tablename__ = 'image'
    id = db.Column(db.Integer, primary_key=True)
    url=db.Column(db.String)
    come_from = db.Column(db.Integer)
    delete_time=db.Column(db.DateTime,default=datetime.now())
    update_time=db.Column(db.DateTime,default=datetime.now())
    def totalUrl(self):
        url=current_app.config.get('IMG_PREFIX')+self.url
        return url



class Theme_Product(db.Model):
    __tablename__ = 'theme_product'
    theme_id=db.Column(db.Integer,db.ForeignKey('theme.id'), primary_key=True)
    product_id=db.Column(db.Integer,db.ForeignKey('product.id'), primary_key=True)
class Theme(db.Model):
    __tablename__ = 'theme'
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String)
    description=db.Column(db.String)
    topic_img_id = db.Column(db.Integer,db.ForeignKey('image.id'))
    topic_img=db.relationship('Image',backref='topic_theme',uselist=False,foreign_keys=[topic_img_id])
    head_img_id=db.Column(db.Integer,db.ForeignKey('image.id'))
    head_img=db.relationship('Image',backref='head_theme',uselist=False,foreign_keys=[head_img_id])
    productInTheme=db.relationship('Theme_Product',
                                    foreign_keys=[Theme_Product.theme_id],
                                    backref=db.backref('backTheme',lazy='joined'),
                                    lazy='dynamic',
                                    cascade='all,delete-orphan')
    delete_time=db.Column(db.DateTime,default=datetime.now())
    update_time=db.Column(db.DateTime,default=datetime.now())
    def to_json(self):
        theme={
            'id':self.id,
            'name':self.name,
            'description':self.description,
            'topic_img':self.topic_img.totalUrl(),
            'head_img':self.head_img.totalUrl(),
        }
        return theme
    def detail(self,id):
        f=self.productInTheme.filter_by(theme_id=id).all()
        return f
class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String)
    price= db.Column(db.Numeric(6, 2))
    stock=db.Column(db.Integer)
    category_id = db.Column(db.Integer)
    main_img_url = db.Column(db.String)
    come_from=db.Column(db.Integer)
    summary=db.Column(db.String)
    img_id=db.Column(db.String)
    themeOfProduct=db.relationship('Theme_Product',
                            foreign_keys=[Theme_Product.product_id],
                            backref=db.backref('backProduct', lazy='joined'),
                            lazy='dynamic',
                            cascade='all,delete-orphan')

    product_image = db.relationship('Product_Image', backref='backproduct',lazy='dynamic')
    product_property= db.relationship('Product_Property', backref='backproduct',lazy='dynamic')
    delete_time=db.Column(db.DateTime,default=datetime.now())
    update_time=db.Column(db.DateTime,default=datetime.now())
    create_time=db.Column(db.DateTime,default=datetime.now())
    def to_json(self):
        product={
            'id':self.id,
            'name':self.name,
            'price':str(self.price),
            'stock':self.stock,
            'category_id':self.category_id,
            'main_img_url':current_app.config.get('IMG_PREFIX')+self.main_img_url,
            'come_from':self.come_from,
            'summary':self.summary
        }
        return product
class Product_Image(db.Model):
    __tablename__ = 'product_image'
    id = db.Column(db.Integer, primary_key=True)
    img_id=db.Column(db.Integer,db.ForeignKey('image.id'))
    img = db.relationship('Image', backref='product_image', uselist=False,foreign_keys=[img_id])
    delete_time = db.Column(db.DateTime, default=datetime.now())
    order=db.Column(db.Integer)
    product_id=db.Column(db.Integer,db.ForeignKey('product.id'))

    def to_json(self):
        product_image={
            'id':self.id,
            'img':self.img.totalUrl(),
            'order':self.order
        }
        return product_image
class Product_Property(db.Model):
    __tablename__ = 'product_property'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    detail= db.Column(db.String)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    delete_time = db.Column(db.DateTime, default=datetime.now())
    update_time = db.Column(db.DateTime, default=datetime.now())
    def to_json(self):
        product_property={
            'id':self.id,
            'name':self.name,
            'detail':self.detail
        }
        return product_property

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    topic_img_id = db.Column(db.Integer, db.ForeignKey('image.id'))
    topic_img = db.relationship('Image', backref='backCategory', uselist=False)
    delete_time = db.Column(db.DateTime, default=datetime.now())
    update_time = db.Column(db.DateTime, default=datetime.now())
    def to_json(self):
        category={
            'id':self.id,
            'name':self.name,
            'description':self.description,
            'topic_img':self.topic_img.totalUrl()
        }
        return category
class User(db.Model):
    __tablename__='user'
    id = db.Column(db.Integer, primary_key=True)
    openid=db.Column(db.String)
    nickname = db.Column(db.String,default=None)
    extend=db.Column(db.String,default=None)
    adddress=db.relationship('Address',backref='user',lazy='dynamic')
    order = db.relationship('Order', backref='user', lazy='dynamic')
    delete_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now)
    create_time=db.Column(db.DateTime, default=datetime.now)
class Address(db.Model):
    __tablename__ = 'user_address'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    mobile = db.Column(db.String)
    province = db.Column(db.String)
    city = db.Column(db.String)
    country = db.Column(db.String)
    detail=db.Column(db.String)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    delete_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now)
    def to_json(self):
        address={
            'name':self.name,
            'mobile':self.mobile,
            'province':self.province,
            'city':self.city,
            'country':self.country,
            'detail':self.detail
        }
        return address
class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    order_no=db.Column(db.String)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    total_price=db.Column(db.Numeric(6, 2))
    status=db.Column(db.Integer,default=1)
    snap_img=db.Column(db.String)
    snap_name=db.Column(db.String)
    total_count=db.Column(db.Integer)
    snap_items=db.Column(db.Text)
    snap_address=db.Column(db.String)
    prepay_id=db.Column(db.String)
    delete_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now)
    create_time = db.Column(db.DateTime, default=datetime.now)
    def to_json(self):
        order={
            'order_no':self.order_no,
            'total_price':str(self.total_price),
            'status':self.status,
            'snap_img':self.snap_img,
            'snap_name':self.snap_name,
            'total_count':self.total_count,
            'snap_items':json.loads(self.snap_items),
            'snap_address':json.loads(self.snap_address),
            'create_time':str(self.create_time)
        }
        return order


