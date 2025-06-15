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
        self.items_count = total_items

    def result(self):
        # Calculate total pages
        total_pages = math.ceil(self.items_count / self.page_size)  # Use math.ceil to round up

        # Calculate the items to return for the current page
        start = (self.page - 1) * self.page_size
        end = start + self.page_size
        page_items = self.items[start:end]

        return PaginationResult(
            page=self.page,
            page_size=self.page_size,
            total_pages=total_pages,
            total_items=self.items_count,
            items=page_items,
        )