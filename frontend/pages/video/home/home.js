Page({
  /**
   * 页面的初始数据   短剧类型：0-短剧 2-合集 3-影视剧 10-电影
   */
  data: {
    item_list:[],
    channel_list:[
      {'id':999, 'name':'推荐'},
      {'id':0, 'name':'短剧'},
      {'id':10, 'name':'电影'},
      {'id':3, 'name':'影视剧'}
    ],
    current_channel: 999,
    video_type: [0, 3, 10],
    page_index:0,
    page_size:12,

    scroll_top: 0, //滚动条高度
    // 定义顶部栏-
    page_show:false,
    navHeight: '',
    menuButtonInfo: {},
    searchMarginTop: 0, // 搜索框上边距
    searchWidth: 0, // 搜索框宽度
    searchHeight: 0 ,// 搜索框高度
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    this.func_get_item_list()  // 获取物品列表
    // 自定义首页顶部
    var systeminfo=wx.getSystemInfoSync()
    //console.log(systeminfo.windowHeight)
    this.setData({
      movehight:systeminfo.windowHeight,
      movehight2:systeminfo.windowHeight-100
    })
    this.setData({
      menuButtonInfo: wx.getMenuButtonBoundingClientRect()
    })
    // console.log(this.data.menuButtonInfo)
    const { top, width, height, right } = this.data.menuButtonInfo
    wx.getSystemInfo({
      success: (res) => {
        const { statusBarHeight } = res
        const margin = top - statusBarHeight
        this.setData({
          navHeight: (height + statusBarHeight + (margin * 2)),
          searchMarginTop: statusBarHeight + margin, // 状态栏 + 胶囊按钮边距
          searchHeight: height,  // 与胶囊按钮同高
          searchWidth: right - width -40// 胶囊按钮右边坐标 - 胶囊按钮宽度 = 按钮左边可使用宽度
        })
      }
    })
  },

  // 获取物品列表
  func_get_item_list: function (cb){
    // console.log("++++++++111111111111111111111111111111+++++++")
    const url_pre = getApp().globalData.apiUrl
    wx.request({
      url: url_pre + 'video/drama/square',
      method:'POST',
      header :{'Content-Type': 'application/json'},
      data : {
        'page_index': this.data.page_index,
        'page_size': this.data.page_size,
        'video_type':this.data.video_type
      },
      success: res => {
        // 替换掉内容中特殊字符串
        console.log("+++++++++", res)
        const deal_res = typeof res.data === 'string' ? JSON.parse(res.data.replace(/NaN/g, 'null')): res.data
        const item_list_batch = deal_res.res.data
        console.log("+++++++++++++++++++++item_list_batch++++++++++++++", typeof(item_list_batch), item_list_batch, this.data.current_channel)
        if (item_list_batch.length in [null, 0]){
            wx.showModal({
                title: '提示',
                content: '本频道已经没有内容，切换到其他频道看看'
              })
        }
        this.setData({item_list: [...this.data.item_list, ...item_list_batch]})
      }
    })

  },

  // 获取好看视频
  fun_get_hao_kan_item_list: function (cb){
    // 获取好看短视频
    console.log('=====')
  },

  // 去详情页
  func_goto_item_details_page:function (params) {
    const item_info = params.currentTarget.dataset.item_detail_home
    const item_info_str =  JSON.stringify({'drama_id': item_info.drama_id})
    wx.navigateTo({
      // url: '/pages/video/index?item_id='+item,
      url: '/pages/video/details_single/index?item_info='+item_info_str,
    })
  },

  // 去搜索页
  func_goto_search_page(e) {
    wx.navigateTo({url: '/pages/video/search/index'})
  },

  // 用户点击某个channel，  切换选项卡，需要重置的数据
  select_channel:function(e){
    this.setData({
      item_list:[],
      current_channel: e.target.dataset.id,
      page_index:0,
      video_type: e.target.dataset.id === 999? [0, 3, 10] : [e.target.dataset.id]

    })
    this.func_get_item_list() // 重新发起数据请求
  },

  // 去物品详情页
  goto_goods_detail:function (params) {
    const item = params.currentTarget.dataset.goods_detail_home
    wx.navigateTo({
    url: '/pages/shop/goods/details-jd/index?goods_info=' + JSON.stringify({'skuId': item.item_id})
    })
  },

  // 下拉刷新，需要重置的数据
  onPullDownRefresh() {
    this.setData({
      item_list:[],
      page_index: 1
    })
    // 重新发起数据请求 ,当 1 完成后，执行 2
    this.func_get_item_list().then(() => {
      wx.stopPullDownRefresh()
    })
  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom() {
    this.data.page_index += 1  // 页码自增
    this.func_get_item_list()  // 请求下一页数据
  },

  // 获取滚动条当前位置
  onPageScroll: function (e) {
    if (e.scrollTop >= 0) {
      this.setData({
        floorstatus: true,
        scrollTop: e.scrollTop
      });
    } else {
      this.setData({
        floorstatus: false
      });
    }
  },

  //回到顶部
  go_top: function (e) {  // 一键回到顶部
    if (wx.pageScrollTo) {
      wx.pageScrollTo({
        scrollTop: 0
      })
    } else {
      wx.showModal({
        title: '提示',
        content: '当前微信版本过低，无法使用该功能，请升级到最新微信版本后重试。'
      })
    }
  }

})