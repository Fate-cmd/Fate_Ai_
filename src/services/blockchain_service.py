from solana.rpc.api import Client
from solana.transaction import Transaction
from solana.keypair import Keypair
from solana.system_program import TransferParams, transfer
from ..core.config import settings
from typing import Optional, Dict, Any

class BlockchainService:
    def __init__(self):
        self.client = Client(settings.SOLANA_RPC_URL)
        self.network = settings.SOLANA_NETWORK

    def get_balance(self, wallet_address: str) -> float:
        try:
            response = self.client.get_balance(wallet_address)
            if response["result"]["value"] is not None:
                return response["result"]["value"] / 1e9  # Convert lamports to SOL
            return 0.0
        except Exception as e:
            print(f"Error getting balance: {str(e)}")
            return 0.0

    def create_wallet(self) -> Dict[str, Any]:
        try:
            keypair = Keypair()
            return {
                "public_key": str(keypair.public_key),
                "private_key": keypair.seed.hex()
            }
        except Exception as e:
            print(f"Error creating wallet: {str(e)}")
            return {}

    def transfer_sol(self, from_wallet: str, to_wallet: str, amount: float) -> Optional[str]:
        try:
            # Convert SOL to lamports
            lamports = int(amount * 1e9)
            
            # Create transaction
            transaction = Transaction()
            
            # Add transfer instruction
            transfer_ix = transfer(
                TransferParams(
                    from_pubkey=from_wallet,
                    to_pubkey=to_wallet,
                    lamports=lamports
                )
            )
            transaction.add(transfer_ix)
            
            # Sign and send transaction
            result = self.client.send_transaction(transaction)
            return result["result"]
        except Exception as e:
            print(f"Error transferring SOL: {str(e)}")
            return None

    def get_transaction_history(self, wallet_address: str) -> list:
        try:
            response = self.client.get_signatures_for_address(wallet_address)
            return response["result"]
        except Exception as e:
            print(f"Error getting transaction history: {str(e)}")
            return [] 