from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from typing import Dict


def get_prev_next(cur_page):
    prev_url = ""
    next_url = ""

    if cur_page.has_previous():
        prev_url = "?page={}".format(cur_page.previous_page_number())
    if cur_page.has_next():
        next_url = "?page={}".format(cur_page.next_page_number())
    return prev_url, next_url


def has_some_pages(page):
    return page.has_other_page()


def get_page_num(request) -> int:
    return request.GET.get('page', 1)


def paginate(objects_list, request, per_page=10) -> dict:
    paginator = Paginator(objects_list, per_page)

    page = request.GET.get('page', 1)

    cur_page = paginator.get_page(page)

    print(page, cur_page)

    prev_url, next_url = get_prev_next(cur_page)

    is_paginated = cur_page.has_other_pages()

    content = {
        'page_object': cur_page,
        'is_paginated': is_paginated,
        'prev_url': prev_url,
        'next_url': next_url
    }

    return content
