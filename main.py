import asyncio
import random
from mnemonic import Mnemonic
from eth_account import Account
import requests

Account.enable_unaudited_hdwallet_features()

# API keys untuk layanan blockchain
ETHERSCAN_API_KEY = "your_etherscan_api_key"
BSCSCAN_API_KEY = "your_bscscan_api_key"
POLYGONSCAN_API_KEY = "your_polygonscan_api_key"

# Fungsi untuk log pesan
def log_message(message, level="info"):
    print(f"[{level.upper()}] {message}")

# Fungsi untuk membuat seed phrase
def generate_seed_phrase():
    mnemo = Mnemonic("english")
    strength = 256 if random.random() > 0.5 else 128
    return mnemo.generate(strength)

# Fungsi untuk mengambil saldo menggunakan API
def get_balance(address, network):
    base_urls = {
        "etherscan": f"https://api.etherscan.io/api",
        "bscscan": f"https://api.bscscan.com/api",
        "polygonscan": f"https://api.polygonscan.com/api",
    }

    api_keys = {
        "etherscan": ETHERSCAN_API_KEY,
        "bscscan": BSCSCAN_API_KEY,
        "polygonscan": POLYGONSCAN_API_KEY,
    }

    url = base_urls[network]
    params = {
        "module": "account",
        "action": "balance",
        "address": address,
        "tag": "latest",
        "apikey": api_keys[network],
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()
        if data["status"] == "1":
            balance = int(data["result"]) / 10**18  # Convert Wei to Ether
            return balance
    except Exception as e:
        log_message(f"Error fetching balance from {network}: {e}", "error")
    return 0.0

# Fungsi utama untuk brute force
async def run_bruteforce():
    while True:
        try:
            seed_phrase = generate_seed_phrase()
            account = Account.from_mnemonic(seed_phrase)

            eth_balance = get_balance(account.address, "etherscan")
            bnb_balance = get_balance(account.address, "bscscan")
            matic_balance = get_balance(account.address, "polygonscan")

            log_message(f"👾 Address: {account.address}", "info")
            log_message(f"💬 Mnemonic: {seed_phrase}", "info")
            log_message(f"🔑 Private key: {account.key.hex()}", "info")
            log_message(f"🤑 ETH Balance: {eth_balance:.6f} ETH", "info")
            log_message(f"🤑 BNB Balance: {bnb_balance:.6f} BNB", "info")
            log_message(f"🤑 MATIC Balance: {matic_balance:.6f} MATIC", "info")

            if eth_balance > 0 or bnb_balance > 0 or matic_balance > 0:
                log_message(f"🎉 Found a wallet with a non-zero balance!", "success")
                with open("wallets.txt", "a") as file:
                    file.write(
                        f"👾 Address: {account.address}\n"
                        f"💬 Mnemonic: {seed_phrase}\n"
                        f"🔑 Private key: {account.key.hex()}\n"
                        f"🤑 ETH Balance: {eth_balance:.6f} ETH\n"
                        f"🤑 BNB Balance: {bnb_balance:.6f} BNB\n"
                        f"🤑 MATIC Balance: {matic_balance:.6f} MATIC\n\n"
                    )
            else:
                log_message(f"👎 No luck this time.", "warning")

            # Tambahkan baris kosong untuk memisahkan hasil log
            print("")

            await asyncio.sleep(1)

        except Exception as e:
            log_message(f"An error occurred: {e}", "error")

# Jalankan brute force
if __name__ == "__main__":
    asyncio.run(run_bruteforce())
