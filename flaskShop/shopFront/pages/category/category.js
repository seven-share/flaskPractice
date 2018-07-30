// pages/category/category.js
import { Category } from 'category-model.js'
var category = new Category();
Page({

  /**
   * 页面的初始数据
   */
  data: {
    currentMenuIndex:0,
    loadedData:{}
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    this._loadData()
  },

  _loadData:function(){
    category.getCategoryType((categoryData)=>{
      this.setData({
        catagoryTypeArr:categoryData
      })
      category.getProductsByCategory(categoryData[0].id,(data)=>{
        var dataObj={
          products:data,
          topImgUrl:categoryData[0].topic_img,
          title:categoryData[0].name
        }
        this.setData({
          categoryProducts:dataObj
        })

        this.data.loadedData[0]=dataObj
      })
    })
  },
  // 判断当前分类下的商品数据是否已经被加载
  isLoadedData:function(index){
    if(this.data.loadedData[index]){
      return true;
    }
    return false;
  },
  changeCategory:function(event){
    var id = category.getDataSet(event,'id');
    var index = category.getDataSet(event, 'index');
    this.setData({
      currentMenuIndex: index
    })
    if (!this.isLoadedData(index)){
      // 如果没有加载当前列表下的数据，请求服务器
      category.getProductsByCategory(id, (data) => {
        var dataObj = {
          products: data,
          topImgUrl: this.data.catagoryTypeArr[index].topic_img,
          title: this.data.catagoryTypeArr[index].name
        }
        this.setData({
          categoryProducts: dataObj
        })
        this.data.loadedData[index] = dataObj
      })
    }
    else{
      this.setData({
        categoryProducts: this.data.loadedData[index]
      })
    }
    
  },
  onProductsItemTap:function(event){
    var id = category.getDataSet(event, 'id');
    wx.navigateTo({
      url: '../product/product?id='+id
    })
  }
})