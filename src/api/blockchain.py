from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from pydantic import BaseModel

from ..core.database import get_db
from ..services.blockchain_service import BlockchainService
from ..models.user import User
from .auth import get_current_user

router = APIRouter()
blockchain_service = BlockchainService()

class TransferRequest(BaseModel):
    to_wallet: str
    amount: float

@router.post("/wallet/create")
async def create_wallet(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    wallet = blockchain_service.create_wallet()
    if not wallet:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create wallet"
        )
    return wallet

@router.get("/wallet/balance")
async def get_wallet_balance(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> float:
    if not current_user.wallet_address:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No wallet address found"
        )
    return blockchain_service.get_balance(current_user.wallet_address)

@router.post("/wallet/transfer")
async def transfer_sol(
    transfer_request: TransferRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    if not current_user.wallet_address:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No wallet address found"
        )
    
    transaction_hash = blockchain_service.transfer_sol(
        current_user.wallet_address,
        transfer_request.to_wallet,
        transfer_request.amount
    )
    
    if not transaction_hash:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Transfer failed"
        )
    
    return {"transaction_hash": transaction_hash}

@router.get("/wallet/transactions")
async def get_transaction_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> List[Dict[str, Any]]:
    if not current_user.wallet_address:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No wallet address found"
        )
    return blockchain_service.get_transaction_history(current_user.wallet_address) 