def apply_sort(queryset, sort):
    if sort == "price_asc":
        return queryset.order_by("price")

    elif sort == "price_desc":
        return queryset.order_by("-price")

    else:
        return queryset.order_by("-id")