from pydantic.v1 import BaseModel


class TestAttributes(BaseModel):
    title: str
    suite_id: str = None
    # the value is not present when we get all tests.
    description: str = None


class Test(BaseModel):
    type: str
    attributes: TestAttributes
    id: str = None
