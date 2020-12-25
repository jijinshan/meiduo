from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from goods.models import GoodsCategory, SKU
from goods.utils import get_breadcrumb


# GET /list/(?P<category_id>\d+)/skus/
class SKUListView(View):
    def get(self, request, category_id):
        page = request.GET.get("page", 1)
        page_size = request.GET.get("page_size", 10)
        ordering = request.GET.get("ordering", "-create_time")
        try:
            cat3 = GoodsCategory.objects.get(id=category_id)
        except Exception as e:
            return JsonResponse({"code": 400,
                                 "message": "查询不到此数据"})
        try:
            breadcrumb = get_breadcrumb(cat3)
        except Exception as e:
            return JsonResponse({"code": 400,
                                 "message": "获取面包屑导航数据出错"})
        try:
            skus = SKU.objects.filter(category_id=category_id,
                                      is_launched=True).order_by(ordering)
        except Exception as e:
            return JsonResponse({"code": 400,
                                 "message": "分类SKU商品数据获取出错"})
        paginator = Paginator(skus, page_size)
        result = paginator.get_page(page)
        sku_li = []
        for sku in result:
            sku_li.append({
                "id": sku.id,
                "name": sku.name,
                "price": sku.price,
                "comments": sku.comments,
                "default_image_url": "http://192.168.19.131:8888/" + sku.default_image.name
            })
        return JsonResponse({"code": 0,
                             "message": "OK",
                             "breadcrumb": breadcrumb,
                             "count": paginator.num_pages,
                             "list": sku_li})


class SKUHotView(View):
    def get(self, request, category_id):
        try:
            cat3 = GoodsCategory.objects.get(id=category_id)
        except Exception as e:
            return JsonResponse({"code": 400,
                                 "message": "查询不到此数据"})
        try:
            skus = SKU.objects.filter(category_id=category_id,
                                      is_launched=True).order_by("-sales")
        except Exception as e:
            return JsonResponse({"code": 400,
                                 "message": "分类SKU商品数据获取出错"})
        hot_skus = []
        i = 0
        for sku in skus:
            if i < 2:
                hot_skus.append({
                    "id": sku.id,
                    "name": sku.name,
                    "price": sku.price,
                    "default_image_url": "http://192.168.19.131:8888/" + sku.default_image.name
                })
                i += 1
        return JsonResponse({"code": 0,
                             "message": "OK",
                             "hot_skus": hot_skus})
