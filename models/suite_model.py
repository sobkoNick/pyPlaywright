from pydantic import BaseModel


class SuiteAttributes(BaseModel):
    title: str
    test_count: int = None
    # the value is not present when we get all suites.
    description: str = None


class Suite(BaseModel):
    type: str
    attributes: SuiteAttributes
    id: str = None
