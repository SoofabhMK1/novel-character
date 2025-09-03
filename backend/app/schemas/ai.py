from pydantic import BaseModel
from typing import Optional

class AIGenerationRequest(BaseModel):
    prompt: str
    use_proxy: bool = False
    proxy_url: Optional[str] = None