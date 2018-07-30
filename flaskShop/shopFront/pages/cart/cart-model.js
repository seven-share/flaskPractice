import { Base } from '../../utils/base.js'
class Cart extends Base{
  constructor(){
    super();
    this._storageKeyName='cart';
  }
  
  // 加入购物车
  // 如果没有该商品，则直接添加一条新的购物记录，数量为count
  // 如果有，则只将相应的数量加上counts
  // @params
  // item - {object} 商品对象
  // coutns - {int} 数量
  add(item,counts){
    var cartData=this.getCartDataFromLocal();
    var isHasInfo=this._isHasThatOne(item.id,cartData)
    if(isHasInfo.index==-1){
      item.counts=counts;
      item.selectStatus=true; //设置选中状态
      cartData.push(item)
    }else{
      cartData[isHasInfo.index].counts+=counts
    }
    wx.setStorageSync(this._storageKeyName, cartData )

  }

  /*本地缓存 保存／更新*/
  execSetStorageSync(data) {
    wx.setStorageSync(this._storageKeyName, data);
  };

  // 从缓存中读取购物车数据
  getCartDataFromLocal(flag){
    var res=wx.getStorageSync(this._storageKeyName);
    if(!res){
      res=[]
    }
    if(flag){
      var newRes=[]
      for(let i=0;i<res.length;i++){
        if(res[i].selectStatus){
          newRes.push(res[i])
        }
      }
      res=newRes
    }
    return res
  }

  // 计算购物车内商品总数量
  // flag true 考虑商品选择状态
  getCartTotalCounts(flag){
    var data=this.getCartDataFromLocal()
    var counts=0
    for(let i=0;i<data.length;i++){
      if (flag) {
        if (data[i].selectStatus) {
          counts += data[i].counts
        }
      }else{
        counts += data[i].counts
      }
    }
    return counts
  }
  // 判断某个商品是否已经被添加入购物车，如果添加过，则返回该商品数据，和在缓存数组中的index
  _isHasThatOne(id,arr){
    var item
    var result={index:-1}
    for(let i=0;i<arr.length;i++){
      item=arr[i]
      if(item.id==id){
        result={
          index:i,
          data:item
        };
        break;
      }
    }
    return result;
  }

  _changeCounts(id,counts){
    var cartData = this.getCartDataFromLocal();
    var hasInfo = this._isHasThatOne(id, cartData)
    if (hasInfo.index != -1) {
      if (hasInfo.data.counts > 1) {
        cartData[hasInfo.index].counts += counts;
      }
    }
    //更新本地缓存
    wx.setStorageSync(this._storageKeyName, cartData); 
  }

  addCounts(id){
    this._changeCounts(id,1)
  }
  cutCounts(id){
    this._changeCounts(id, -1)
  }

  delete(ids){
    if(!(ids instanceof Array)){
      ids=[ids]
    }
    var cartData = this.getCartDataFromLocal();

    for(let i=0;i<ids.length;i++){
      var hasInfo = this._isHasThatOne(ids[i], cartData)
      if(hasInfo.index!=-1){
        cartData.splice(hasInfo.index,1)
      }
    }
    wx.setStorageSync(this._storageKeyName, cartData); 
  }
}
export {Cart}