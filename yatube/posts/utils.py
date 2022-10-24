from django.core.paginator import Paginator

COUNT_POSTS = 10


def pagination(request, some_obj_list) -> Paginator.page:
    """Создание объекта типа paginator с данными для вывода на страницу"""
    paginator = Paginator(some_obj_list, COUNT_POSTS)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)
