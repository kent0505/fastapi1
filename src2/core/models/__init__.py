from sqlalchemy.ext.asyncio    import AsyncSession
from sqlalchemy                import select, desc
from typing                    import List
from pydantic                  import BaseModel
from src.core.models.db_helper import db_helper
from src.core.models.base      import *