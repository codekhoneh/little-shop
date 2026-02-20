from shop.models import Collection

def our_collections(request):
    collection=Collection.objects.filter(is_active=True)[:4]
    return{
        "our_collections":collection
    }