from django.db import models

from goods.models import SKU
from meiduo_mall.utils.base_model import BaseModel
from users.models import User, Address


class OrderInfo(BaseModel):
    """订单信息"""
    order_id = models.CharField(max_length=64, primary_key=True,
                                verbose_name="订单号")
    # 一对多关联属性
    user = models.ForeignKey(User, related_name="orders",
                             on_delete=models.PROTECT, verbose_name="下单用户")
    # 一对多关联属性
    address = models.ForeignKey(Address, on_delete=models.PROTECT,
                                verbose_name="收货地址")
    total_count = models.IntegerField(default=1, verbose_name="商品总数")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2,
                                       verbose_name="商品总金额")
    freight = models.DecimalField(max_digits=10, decimal_places=2,
                                  verbose_name="运费")
    # 1：货到付款 2：支付宝
    pay_method = models.SmallIntegerField(default=1, verbose_name="支付方式")
    # 1：待支付 2：待发货 3：待收货 4：待评价 5：已完成 6：已取消
    status = models.SmallIntegerField(default=1, verbose_name="订单状态")

    class Meta:
        db_table = "tb_order_info"
        verbose_name = '订单基本信息'

    def __str__(self):
        return self.order_id


class OrderGoods(BaseModel):
    """订单商品"""
    # 一对多关联属性
    order = models.ForeignKey(OrderInfo, related_name='skus',
                              on_delete=models.CASCADE, verbose_name="订单")
    # 一对多关联属性
    sku = models.ForeignKey(SKU, on_delete=models.PROTECT, verbose_name="订单商品")
    count = models.IntegerField(default=1, verbose_name="数量")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="单价")
    comment = models.TextField(default="", verbose_name="评价信息")
    # 0：0分 1：20分 3：60分 4：80分 5：100分
    score = models.SmallIntegerField(default=5, verbose_name='满意度评分')
    is_anonymous = models.BooleanField(default=False, verbose_name='是否匿名评价')
    is_commented = models.BooleanField(default=False, verbose_name='是否评价完成')

    class Meta:
        db_table = "tb_order_goods"
        verbose_name = '订单商品'

    def __str__(self):
        return self.sku.name