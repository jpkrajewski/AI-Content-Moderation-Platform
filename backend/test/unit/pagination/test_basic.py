from moderation.pagination.basic import BasicPagination, PaginationResult
from math import ceil

def test_basic_pagination_result():
    items = ['item1', 'item2', 'item3']
    total_items = 10
    page = 1
    page_size = 3

    paginator = BasicPagination(
        page_size=page_size,
        page=page,
        items=items,
        total_items=total_items
    )

    result = paginator.result()

    assert isinstance(result, PaginationResult)
    assert result.page == page
    assert result.page_size == page_size
    assert result.total_items == total_items
    assert result.items == items
    assert result.total_pages == ceil(total_items / page_size)

