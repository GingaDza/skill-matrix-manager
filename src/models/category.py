from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Category:
    id: int
    name: str
    parent_id: Optional[int] = None
    children: List['Category'] = None
    
    def __post_init__(self):
        if self.children is None:
            self.children = []
