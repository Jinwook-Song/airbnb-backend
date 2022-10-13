from categories.models import Category
from categories.serializers import CategorySerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view()
def categories(req):
    all_categories = Category.objects.all()
    # CategorySerializer는 하나의 category에 대해서 번역을 하고 있기 때문에
    # 리스트를 번역하기 위해 many 옵션 필요
    serializers = CategorySerializer(all_categories, many=True)
    return Response(
        {
            "ok": True,
            "categories": serializers.data,
        },
    )
