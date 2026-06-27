import os
import requests
import random
import time
import json
from faker import Faker
from keep_alive import live
from datetime import datetime

fake = Faker()

# Get from environment variables
BOT_TOKEN = os.environ.get('BOT_TOKEN', '8802180200:AAHcgil1mIstzrU6xPmP5oEK6lVBywiyOFs')
CHAT_ID = int(os.environ.get('CHAT_ID', -1004480875479))

# Enhanced card prefixes with premium card indicators
CARD_PREFIXES = {
    'Visa': {
        'prefixes': ['4'],
        'premium': ['4532', '4539', '4556', '4916', '4929', '4484', '4716'],  # Premium Visa
        'level': ['Classic', 'Gold', 'Platinum', 'Signature', 'Infinite']
    },
    'Mastercard': {
        'prefixes': ['5', '2'],
        'premium': ['2221', '2223', '2224', '2230', '2234', '2244', '2250', '2254', '2260', '2263', '2270', '2273', '2280', '2285', '2290', '2299', '2300', '2322', '2330', '2340', '2350', '2360', '2370', '2380', '2390', '2400', '2410', '2420', '2430', '2440', '2450', '2460', '2470', '2480', '2490', '2500', '2510', '2520', '2530', '2540', '2550', '2560', '2570', '2580', '2590', '2600', '2610', '2620', '2630', '2640', '2650', '2660', '2670', '2680', '2690', '2700', '2710', '2720', '2730', '2740', '2750', '2760', '2770', '2780', '2790', '2800', '2810', '2820', '2830', '2840', '2850', '2860', '2870', '2880', '2890', '2900', '2910', '2920', '2930', '2940', '2950', '2960', '2970', '2980', '2990'],
        'level': ['Standard', 'Gold', 'Platinum', 'World', 'World Elite']
    },
    'American Express': {
        'prefixes': ['34', '37'],
        'premium': ['3400', '3700', '3714', '3727', '3766'],  # Premium Amex
        'level': ['Green', 'Gold', 'Platinum', 'Centurion']
    },
    'Discover': {
        'prefixes': ['6011', '65'],
        'premium': ['6011', '6221', '6222', '6223', '6224', '6225', '6226', '6227', '6228', '6229', '6230', '6231', '6232', '6233', '6234', '6235', '6236', '6237', '6238', '6239', '6240', '6241', '6242', '6243', '6244', '6245', '6246', '6247', '6248', '6249', '6250', '6251', '6252', '6253', '6254', '6255', '6256', '6257', '6258', '6259', '6260', '6261', '6262', '6263', '6264', '6265', '6266', '6267', '6268', '6269', '6270', '6271', '6272', '6273', '6274', '6275', '6276', '6277', '6278', '6279', '6280', '6281', '6282', '6283', '6284', '6285', '6286', '6287', '6288', '6289', '6290', '6291', '6292', '6293', '6294', '6295', '6296', '6297', '6298', '6299'],
        'level': ['Standard', 'Gold', 'Platinum', 'Miles']
    },
    'JCB': {
        'prefixes': ['35'],
        'premium': ['3528', '3529', '3530', '3531', '3532', '3533', '3534', '3535', '3536', '3537', '3538', '3539', '3540', '3541', '3542', '3543', '3544', '3545', '3546', '3547', '3548', '3549', '3550', '3551', '3552', '3553', '3554', '3555', '3556', '3557', '3558', '3559', '3560', '3561', '3562', '3563', '3564', '3565', '3566', '3567', '3568', '3569', '3570', '3571', '3572', '3573', '3574', '3575', '3576', '3577', '3578', '3579', '3580', '3581', '3582', '3583', '3584', '3585', '3586', '3587', '3588', '3589', '3590', '3591', '3592', '3593', '3594', '3595', '3596', '3597', '3598', '3599'],
        'level': ['Classic', 'Gold', 'Platinum']
    },
    'Diners Club': {
        'prefixes': ['30', '36', '38'],
        'premium': ['3000', '3001', '3002', '3003', '3004', '3005', '3006', '3007', '3008', '3009', '3010', '3011', '3012', '3013', '3014', '3015', '3016', '3017', '3018', '3019', '3020', '3021', '3022', '3023', '3024', '3025', '3026', '3027', '3028', '3029', '3030', '3031', '3032', '3033', '3034', '3035', '3036', '3037', '3038', '3039', '3040', '3041', '3042', '3043', '3044', '3045', '3046', '3047', '3048', '3049', '3050', '3051', '3052', '3053', '3054', '3055', '3056', '3057', '3058', '3059', '3060', '3061', '3062', '3063', '3064', '3065', '3066', '3067', '3068', '3069', '3070', '3071', '3072', '3073', '3074', '3075', '3076', '3077', '3078', '3079', '3080', '3081', '3082', '3083', '3084', '3085', '3086', '3087', '3088', '3089', '3090', '3091', '3092', '3093', '3094', '3095', '3096', '3097', '3098', '3099'],
        'level': ['Standard', 'Gold', 'Platinum']
    },
    'UnionPay': {
        'prefixes': ['62'],
        'premium': ['6200', '6201', '6202', '6203', '6204', '6205', '6206', '6207', '6208', '6209', '6210', '6211', '6212', '6213', '6214', '6215', '6216', '6217', '6218', '6219', '6220', '6221', '6222', '6223', '6224', '6225', '6226', '6227', '6228', '6229', '6230', '6231', '6232', '6233', '6234', '6235', '6236', '6237', '6238', '6239', '6240', '6241', '6242', '6243', '6244', '6245', '6246', '6247', '6248', '6249', '6250', '6251', '6252', '6253', '6254', '6255', '6256', '6257', '6258', '6259', '6260', '6261', '6262', '6263', '6264', '6265', '6266', '6267', '6268', '6269', '6270', '6271', '6272', '6273', '6274', '6275', '6276', '6277', '6278', '6279', '6280', '6281', '6282', '6283', '6284', '6285', '6286', '6287', '6288', '6289', '6290', '6291', '6292', '6293', '6294', '6295', '6296', '6297', '6298', '6299'],
        'level': ['Standard', 'Gold', 'Platinum', 'Diamond']
    }
}

# Premium card types with higher success rates (4, 5, 6 prefixes)
PREMIUM_BINS = [
    # Visa Premium (4)
    '4532', '4539', '4556', '4916', '4929', '4484', '4716',
    # Mastercard Premium (5)
    '2221', '2223', '2230', '2234', '2244', '2250', '2254', '2260',
    '2263', '2270', '2273', '2280', '2285', '2290', '2299', '2300',
    '2322', '2330', '2340', '2350', '2360', '2370', '2380', '2390',
    # Discover Premium (6)
    '6011', '6221', '6222', '6223', '6224', '6225', '6226', '6227',
    '6228', '6229', '6230', '6231', '6232', '6233', '6234', '6235',
    # Amex Premium
    '3700', '3714', '3727', '3766',
    # JCB Premium
    '3528', '3529', '3530', '3531', '3532', '3533', '3534', '3535'
]

def generate_premium_card_number(card_type=None):
    """Generate premium card number with higher success rate"""
    if card_type and card_type in CARD_PREFIXES:
        # Use premium prefixes for the specific card type
        if random.random() < 0.7:  # 70% chance of premium
            prefix = random.choice(CARD_PREFIXES[card_type]['premium'])
        else:
            prefix = random.choice(CARD_PREFIXES[card_type]['prefixes'])
    else:
        # Random premium card type
        card_type = random.choices(
            list(CARD_PREFIXES.keys()),
            weights=[35, 30, 15, 10, 5, 3, 2],  # Higher weight for Visa, Mastercard
            k=1
        )[0]
        
        if random.random() < 0.75:  # 75% chance of premium
            prefix = random.choice(CARD_PREFIXES[card_type]['premium'])
        else:
            prefix = random.choice(CARD_PREFIXES[card_type]['prefixes'])
    
    if card_type == 'American Express':
        length = 15
    elif card_type == 'Diners Club':
        length = 14
    else:
        length = 16
    
    body = prefix + ''.join([str(random.randint(0, 9)) for _ in range(length - len(prefix) - 1)])
    
    digits = [int(d) for d in body]
    for i in range(len(digits) - 2, -1, -2):
        digits[i] *= 2
        if digits[i] > 9:
            digits[i] -= 9
            
    total_sum = sum(digits)
    check_digit = (10 - (total_sum % 10)) % 10
    
    return body + str(check_digit), card_type

def get_premium_level(card_type):
    """Get premium card level"""
    if card_type in CARD_PREFIXES:
        levels = CARD_PREFIXES[card_type]['level']
        # Weighted random for higher levels
        weights = [15, 25, 30, 20, 10] if len(levels) >= 5 else [10, 30, 35, 25]
        return random.choices(levels, weights=weights[:len(levels)], k=1)[0]
    return "Premium"

def luhn_algorithm(card_number):
    digits = [int(digit) for digit in card_number]
    for i in range(len(digits) - 2, -1, -2):
        digits[i] *= 2
        if digits[i] > 9:
            digits[i] -= 9
    return sum(digits) % 10 == 0

def generate_card_details():
    # Generate premium card
    card_number, card_type = generate_premium_card_number()
    
    # Generate expiry date (further out for premium cards)
    month = str(random.randint(1, 12)).zfill(2)
    year = str(random.randint(26, 35)).zfill(2)  # 2026-2035
    
    if card_type == 'American Express':
        cvv = str(random.randint(1000, 9999)).zfill(4)
    else:
        cvv = str(random.randint(100, 999)).zfill(3)
    
    return f"{card_number}|{month}|{year}|{cvv}", card_type

def get_bin_info(bin_number):
    """Enhanced BIN lookup with multiple sources"""
    try:
        # Primary BIN API
        response = requests.get(f"https://bins.antipublic.cc/bins/{bin_number}", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('brand'):
                return data
    except:
        pass
    
    try:
        # Backup BIN API
        response = requests.get(f"https://lookup.binlist.net/{bin_number}", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('brand'):
                return {
                    'brand': data.get('brand', 'Unknown'),
                    'country': data.get('country', {}).get('numeric', 'US'),
                    'country_name': data.get('country', {}).get('name', 'United States'),
                    'country_flag': data.get('country', {}).get('emoji', '🇺🇸'),
                    'bank': data.get('bank', {}).get('name', 'Unknown Bank'),
                    'level': data.get('scheme', 'Standard'),
                    'type': data.get('type', 'Credit')
                }
    except:
        pass
    
    return None

def send_messages():
    telegram_api = f'https://api.telegram.org/bot{BOT_TOKEN}'
    requests_limit = 1
    pause_duration = 2
    total_cards = 10000000000
    max_retries = 3  # Increased retries
    
    success_count = 0
    premium_count = 0
    
    for i in range(1, total_cards + 1):
        card_details, card_type = generate_card_details()
        card_number = card_details.split('|')[0]
        
        if not luhn_algorithm(card_number):
            print(f"Invalid card at {i}: {card_details} - SKIPPING")
            continue
        
        BIN = card_number[:6]
        card_info = get_bin_info(BIN)
        
        # Default values
        brand = card_type.upper()
        country = 'US'
        country_name = 'United States'
        country_flag = '🇺🇸'
        bank = 'Premium Bank'
        level = get_premium_level(card_type)
        typea = 'Credit'
        
        if card_info:
            brand = card_info.get('brand', card_type).upper()
            country = card_info.get('country', 'US')
            country_name = card_info.get('country_name', 'United States')
            country_flag = card_info.get('country_flag', '🇺🇸')
            bank = card_info.get('bank', 'Premium Bank')
            level = card_info.get('level', get_premium_level(card_type))
            typea = card_info.get('type', 'Credit')
            print(f"✅ BIN {BIN}: {brand} - {bank}")
        else:
            # Check if it's a premium BIN
            if any(BIN.startswith(premium_bin) for premium_bin in PREMIUM_BINS):
                level = random.choice(['Premium', 'Gold', 'Platinum', 'Signature', 'World Elite'])
                bank = random.choice(['Chase', 'Citibank', 'Bank of America', 'Wells Fargo', 'Capital One'])
                print(f"⭐ Premium BIN {BIN}: {brand} - {bank}")
            else:
                print(f"⚠️ Using default info for BIN {BIN}")

        month, year, cvv = card_details.split('|')[1], card_details.split('|')[2], card_details.split('|')[3]
        full_name = fake.name()
        
        # Check if premium card
        is_premium = any(BIN.startswith(premium_bin) for premium_bin in PREMIUM_BINS) or level in ['Platinum', 'Signature', 'World Elite', 'Centurion', 'Diamond']
        if is_premium:
            premium_count += 1
        
        success_count += 1
        
        # Premium UI with enhanced styling
        reply_markup = {
            "inline_keyboard": [
                [
                    {"text": "𝙊𝙒𝙉𝙀𝙍", "url": "https://t.me/Atul_FROXT_73"},
                    {"text": "𝘾𝙃𝘼𝙉𝙉𝙀𝙇", "url": "https://t.me/+gS3I7lo7i98zZjc1"},
                ]
            ]
        }
        
        # Enhanced message with premium indicators
        premium_badge = "⭐ PREMIUM ⭐" if is_premium else "💳 STANDARD"
        status_badge = "✅ 𝗔𝗣𝗣𝗥𝗢𝗩𝗘𝗗 | 𝗟𝗜𝗩𝗘" if is_premium else "✅ 𝗔𝗣𝗣𝗥𝗢𝗩𝗘𝗗"
        
        message = (
            f"\n"
            f" 𝗙𝗥𝗢𝗫𝗧 𝗣𝗥𝗘𝗠𝗜𝗨𝗠 🔥\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"<b>⌖ 𝗖𝗮𝗿𝗱 ⤳</b> <code>{card_details}</code>\n"
            f"⌖ 𝗦𝘁𝗮𝘁𝘂𝘀 ⤳ {status_badge}\n"
            f"⌖ 𝗟𝗲𝘃𝗲𝗹 ⤳ {premium_badge}\n"
            f"⌖ 𝗕𝗶𝗻 ⤳ {BIN}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"<b>⌮ 𝗧𝘆𝗽𝗲 ⤳ </b>  <code>{brand} • {typea}</code>\n"
            f"<b>⌮ 𝗕𝗮𝗻𝗸 ⤳ </b>  <code>{bank}</code>\n"
            f"<b>⌮ 𝗖𝗼𝘂𝗻𝘁𝗿𝘆 ⤳ </b>  <code>{country_name} [{country_flag}]</code>\n"
            f"<b>⌮ 𝗟𝗲𝘃𝗲𝗹 ⤳ </b>  <code>{level}</code>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"<b>⌮ 𝗕𝗜𝗡 𝗜𝗻𝗳𝗼 ⤳ </b>  <code>{card_number[:6]}xxxx|{month}|{year}|cvv</code>\n"
            f"<b>⌮ 𝗛𝗼𝗹𝗱𝗲𝗿 ⤳ </b>  <code>{full_name}</code>\n"
            f"<b>⌮ 𝗩𝗮𝗹𝗶𝗱 ⤳ </b>  <code>{month}/{year}</code>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📊 𝗦𝘁𝗮𝘁𝘀: {success_count}/{total_cards} | ⭐ Premium: {premium_count}\n"
        )

        retry_count = 0
        message_sent = False
        
        while retry_count < max_retries and not message_sent:
            try:
                data = {
                    'chat_id': CHAT_ID,
                    'text': message,
                    'parse_mode': 'HTML',
                    'reply_markup': json.dumps(reply_markup)
                }
                response = requests.post(f'{telegram_api}/sendMessage', data=data)
                
                if response.status_code == 200:
                    print(f"✅ Sent card {i}: {card_type} - {card_details} {'⭐' if is_premium else ''}")
                    message_sent = True
                elif response.status_code == 429:
                    retry_after = response.json().get('parameters', {}).get('retry_after', 10)
                    print(f"⚠️ Rate limited. Waiting {retry_after} seconds...")
                    time.sleep(retry_after)
                    retry_count += 1
                else:
                    print(f"❌ Error: {response.text}")
                    retry_count += 1
                    time.sleep(2)
            except Exception as e:
                print(f"❌ Error: {e}")
                retry_count += 1
                time.sleep(2)
        
        if not message_sent:
            print(f"❌ Failed to send card {i} after {max_retries} attempts")

        if i % requests_limit == 0 and i != total_cards:
            time.sleep(pause_duration)
    
    print(f"\n📊 Summary: Sent {success_count} cards, {premium_count} premium cards")

if __name__ == '__main__':
    live()  # Keep alive Flask server
    send_messages()