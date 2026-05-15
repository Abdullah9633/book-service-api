from redis import asyncio
from src.config import my_config

token_blocklist = asyncio.StrictRedis(
    host= my_config.REDIS_HOST,
    port= my_config.REDIS_PORT,
    db= 0
)

JTI_EXPIRY = 3600

async def add_to_blocklist(jti: str):
    await token_blocklist.set(
        name= jti,
        value= "",
        ex= JTI_EXPIRY
    )
    
async def token_in_blocklist(jti: str) -> bool:
    jti_presence = await token_blocklist.get(jti)
    
    return jti_presence is not None



