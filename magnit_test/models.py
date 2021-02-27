from operator import add
from operator import mul
from operator import sub
from operator import truediv
from typing import Literal
from typing import Optional

from pydantic import BaseModel
from pydantic import Field

from magnit_test import utils


class Task(BaseModel):
    # pylint: disable=invalid-name
    x: int
    y: int
    operator: Literal["+", "-", "*", "/"]
    id: str = Field(default_factory=utils.uuid4_str)
    result: Optional[int]
    status: str = "created"

    async def execute(self) -> None:
        """Выполнить операцию (таск)"""
        mapping = {"+": add, "-": sub, "*": mul, "/": truediv}
        self.result = mapping[self.operator](self.x, self.y)
        self.status = "done"
