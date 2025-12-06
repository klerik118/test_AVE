from fastapi import APIRouter, Depends, Query, HTTPException
from redis.asyncio import Redis

from app.redis import get_redis
from app.schemas import Record


router = APIRouter(prefix='/records', tags=['telephone-address'])


@router.get('/get_address_by_number', summary='Get saved address by phone number', response_model=dict)
async def get_address(
    telephon: str = Query(..., regex=r'^\d{6,11}$', description='Enter phone number'), 
    redis_app: Redis = Depends(get_redis)
    ):
    result = await redis_app.get(telephon)
    if result:
        return {'status': 'success', 'number': telephon, 'address': result}
    else:
        raise HTTPException(status_code=404, detail="No such entry")

    
@router.post('', summary='creating record', response_model=dict) 
async def add_record(record: Record, redis_app: Redis = Depends(get_redis)):
    if await redis_app.get(record.number):
        raise HTTPException(status_code=409, detail="this number already exists")
    await redis_app.set(record.number, record.address)
    return {'status': f'Record with number {record.number} successfully created'}


@router.put('', summary='update address', response_model=dict) 
async def update_address(record: Record, redis_app: Redis = Depends(get_redis)):
    if await redis_app.get(record.number):
        await redis_app.set(record.number, record.address)
        return {'status': f'Record with number {record.number} successfully changed'}
    else:
        raise HTTPException(status_code=404, detail="No such entry")
    

@router.delete('', summary='delete record', response_model=dict) #
async def delete_category(
    telephon: str = Query(..., regex=r'^\d{6,11}$', description='Enter phone number'),
    redis_app: Redis = Depends(get_redis)
    ):
    deleted_count = await redis_app.delete(telephon)
    if deleted_count :
        return {'status': f'Record with number {telephon} successfully deleted'}
    else:
        raise HTTPException(status_code=404, detail="No such entry")

    