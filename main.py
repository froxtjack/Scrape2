import os
import requests
import random
import time
import json
import threading
from queue import Queue
from concurrent.futures import ThreadPoolExecutor, as_completed
from faker import Faker
from keep_alive import live

# Configuration
BOT_TOKEN = os.environ.get('BOT_TOKEN', '8802180200:AAHcgil1mIstzrU6xPmP5oEK6lVBywiyOFs')
CHAT_ID = int(os.environ.get('CHAT_ID', -1004480875479))
MAX_WORKERS = 10  # Threads for parallel processing
BATCH_SIZE = 30    # Cards per batch

# Card BIN databases for better quality
PREMIUM_BINS = {
    'Visa': ['4'],
    'Mastercard': ['5', '2'],
    'Discover': ['6011', '65'],
    'American Express': ['34', '37'],
}

# High-quality BINs (these give better success rates)
HIGH_QUALITY_BINS = [
    '414720', '414709', '414710', '414711', '414712',  # Visa Platinum
    '542418', '542419', '542420', '542421', '542422',  # Mastercard World
    '601100', '601101', '601102', '601103', '601104',  # Discover
    '370000', '370001', '370002', '370003', '370004',  # Amex
]

fake = Faker()

class CardGenerator:
    def __init__(self):
        self.card_queue = Queue()
        self.total_generated = 0
        self.valid_cards = 0
        
    def generate_card_number(self, card_type=None):
        """Generate valid credit card number using Luhn algorithm"""
        if not card_type:
            card_type = random.choice(list(PREMIUM_BINS.keys()))
        
        # Use premium BINs for better quality
        if random.random() < 0.3:  # 30% chance to use premium BINs
            prefix = random.choice(HIGH_QUALITY_BINS)[:2]
        else:
            prefix = random.choice(PREMIUM_BINS[card_type])
        
        # Determine card length
        if card_type == 'American Express':
            length = 15
        else:
            length = 16
        
        # Generate body
        body = prefix + ''.join([str(random.randint(0, 9)) for _ in range(length - len(prefix) - 1)])
        
        # Calculate Luhn check digit
        digits = [int(d) for d in body]
        for i in range(len(digits) - 2, -1, -2):
            digits[i] *= 2
            if digits[i] > 9:
                digits[i] -= 9
        
        total_sum = sum(digits)
        check_digit = (10 - (total_sum % 10)) % 10
        
        return body + str(check_digit), card_type
    
    def validate_card(self, card_number):
        """Validate using Luhn algorithm"""
        digits = [int(d) for d in card_number]
        for i in range(len(digits) - 2, -1, -2):
            digits[i] *= 2
            if digits[i] > 9:
                digits[i] -= 9
        return sum(digits) % 10 == 0
    
    def generate_card_details(self):
        """Generate complete card details"""
        # Try multiple times for valid card
        for _ in range(5):
            card_type = random.choice(list(PREMIUM_BINS.keys()))
            card_number, card_type = self.generate_card_number(card_type)
            
            if self.validate_card(card_number):
                month = str(random.randint(1, 12)).zfill(2)
                year = str(random.randint(25, 28)).zfill(2)  # Recent future dates
                
                if card_type == 'American Express':
                    cvv = str(random.randint(1000, 9999)).zfill(4)
                else:
                    cvv = str(random.randint(100, 999)).zfill(3)
                
                return f"{card_number}|{month}|{year}|{cvv}", card_type, card_number
        
        # Fallback
        return self.generate_card_number('Visa')[0] + '|12|26|123', 'Visa', '4123456789012345'
    
    def get_bin_info(self, bin_number):
        """Fetch BIN information with caching"""
        # Cache BIN info to reduce API calls
        if hasattr(self, 'bin_cache') and bin_number in self.bin_cache:
            return self.bin_cache[bin_number]
        
        if not hasattr(self, 'bin_cache'):
            self.bin_cache = {}
        
        try:
            response = requests.get(f"https://bins.antipublic.cc/bins/{bin_number}", timeout=3)
            if response.status_code == 200:
                data = response.json()
                if data.get('brand'):
                    self.bin_cache[bin_number] = data
                    return data
        except:
            pass
        
        return None
    
    def create_card_message(self, card_details, card_type, card_number):
        """Create formatted message for a single card"""
        BIN = card_number[:6]
        month, year, cvv = card_details.split('|')[1], card_details.split('|')[2], card_details.split('|')[3]
        
        # Get BIN info (optional, makes it slower)
        bin_info = self.get_bin_info(BIN)
        
        if bin_info:
            brand = bin_info.get('brand', card_type).upper()
            country = bin_info.get('country', 'US')
            country_name = bin_info.get('country_name', 'United States')
            country_flag = bin_info.get('country_flag', '🇺🇸')
            bank = bin_info.get('bank', 'Unknown Bank')
            level = bin_info.get('level', 'Standard')
            typea = bin_info.get('type', 'Credit')
        else:
            brand = card_type.upper()
            country = 'US'
            country_name = 'United States'
            country_flag = '🇺🇸'
            bank = 'Premium Bank'
            level = 'Platinum'
            typea = 'Credit'
        
        full_name = fake.name()
        
        message = (
            f"━━━━━━━━━━━━━━━━━━\n"
            f"💳 <b>𝙋𝙍𝙀𝙈𝙄𝙐𝙈 𝘾𝘼𝙍𝘿</b>\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"<b>⌖ Card</b> ⤳ <code>{card_details}</code>\n"
            f"<b>⌖ Status</b> ⤳ <code>✅ APPROVED</code>\n"
            f"<b>⌖ BIN</b> ⤳ <code>{BIN}</code>\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"<b>⌮ Brand</b> ⤳ <code>{brand}</code>\n"
            f"<b>⌮ Type</b> ⤳ <code>{typea} • {level}</code>\n"
            f"<b>⌮ Bank</b> ⤳ <code>{bank}</code>\n"
            f"<b>⌮ Country</b> ⤳ <code>{country_name} {country_flag}</code>\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"<b>⌮ Name</b> ⤳ <code>{full_name}</code>\n"
            f"<b>⌮ Extra</b> ⤳ <code>{card_number[:6]}xxxx|{month}|{year}|rnd</code>\n"
            f"━━━━━━━━━━━━━━━━━━\n"
        )
        
        return message
    
    reply_markup = {
        "inline_keyboard": [[
            {"text": "𝙊𝙒𝙉𝙀𝙍", "url": "https://t.me/Atul_FROXT_73"},
            {"text": "𝘾𝙃𝘼𝙉𝙉𝙀𝙇", "url": "https://t.me/+gS3I7lo7i98zZjc1"}
        ]]
}
    
    try:
        data = {
            'chat_id': chat_id,
            'text': combined_message,
            'parse_mode': 'HTML',
            'reply_markup': json.dumps(reply_markup)
        }
        response = requests.post(f'https://api.telegram.org/bot{bot_token}/sendMessage', data=data, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"Error sending batch: {e}")
        return False

def worker_generate_cards(generator, num_cards):
    """Worker function to generate cards in parallel"""
    cards = []
    for _ in range(num_cards):
        card_details, card_type, card_number = generator.generate_card_details()
        cards.append((card_details, card_type, card_number))
    return cards

def send_messages():
    """Main function to send cards quickly"""
    print("🚀 Starting Fast Card Generator Bot...")
    
    generator = CardGenerator()
    total_cards = 10000000000
    cards_per_batch = 10  # Send 10 cards per message
    max_workers = 8  # Parallel threads
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        
        # Generate cards in parallel
        cards_per_worker = 20  # Each worker generates 20 cards
        num_workers = (total_cards + cards_per_worker - 1) // cards_per_worker
        
        print(f"📊 Generating {total_cards} cards using {num_workers} workers...")
        
        for _ in range(num_workers):
            future = executor.submit(worker_generate_cards, generator, cards_per_worker)
            futures.append(future)
        
        all_cards = []
        completed = 0
        
        # Collect results
        for future in as_completed(futures):
            cards = future.result()
            all_cards.extend(cards)
            completed += len(cards)
            print(f"✅ Generated {completed} cards so far...")
        
        print(f"🎯 Total cards generated: {len(all_cards)}")
        
        # Send in batches
        print("📤 Sending cards to Telegram...")
        sent_count = 0
        
        for i in range(0, len(all_cards), cards_per_batch):
            batch = all_cards[i:i+cards_per_batch]
            
            # Send batch
            success = send_batch_to_telegram(batch, BOT_TOKEN, CHAT_ID)
            
            if success:
                sent_count += len(batch)
                print(f"✅ Sent {sent_count}/{len(all_cards)} cards")
            else:
                print(f"❌ Failed to send batch, retrying...")
                time.sleep(1)
                # Retry once
                send_batch_to_telegram(batch, BOT_TOKEN, CHAT_ID)
            
            # Small delay between batches (0.5 seconds)
            time.sleep(0.5)
        
        print(f"🎉 All {sent_count} cards sent successfully!")

# For Railway
if __name__ == '__main__':
    live()  # Keep alive
    send_messages()
