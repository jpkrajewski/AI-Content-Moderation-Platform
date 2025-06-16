import math
from typing import List, Any
from dataclasses import dataclass

@dataclass
class PaginationResult:
    page: int
    page_size: int
    total_pages: int
    total_items: int
    items: List[Any]



class BasicPagination:
    def __init__(self, *, page_size: int, page: int, items: List[Any], total_items: int):
        self.page_size = page_size
        self.page = page
        self.items = items
        self.total_items = total_items

    def result(self) -> PaginationResult:
        total_pages = math.ceil(self.total_items / self.page_size)
        return PaginationResult(
            page=self.page,
            page_size=self.page_size,
            total_pages=total_pages,
            total_items=self.total_items,
            items=self.items,
        )