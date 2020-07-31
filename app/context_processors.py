from .models import Cart

def common(request):
    # 未注文のカート件数を取得
    count = None
    if request.user.is_authenticated:
        count = Cart.objects.filter(user=request.user, ordered=False).count()
    context = {
        'count': count
    }
    return context