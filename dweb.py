import requests
import random
import time
import string
from datetime import datetime

# Random Messages
random_messages = [
    "Hello @everyone, your webhook has be found!",
    "Hey @everyone, please remain calm",
    "Attention @everyone, we have an update!",
    "Greetings @everyone, something new just happened!",
    "@everyone HGKDKHEKDKHFIEOUYHUSDHUHJLHSWIJRIHJFHPWOIJRIHJISOAPWIJTOHSBHGJPEOAWUR",
    "@everyone SJIIJGPDJAWOAWPJHDAWSKHDLAKWPDGPISNKAWNGNDAWQ",
    "@everyone @everyone @here @here WOW SDHUWUAJHSUDHWIAHUSHOTHOEUSHJBJBGJBAWKUHHRUIWASJDJGLAUWEH",
    "@everyone @everyone @everyone @everyone @everyone @everyone @everyone @everyone @everyone @everyone JHDJGHSLJEHJLHDJBNJBAWPIJIJIPOAWIHJHSPWRHHDPAWH",
    "@everyone Hello",
    "@everyone Bye",
    "@everyone What's up!",
    "@everyone Goodbye!"
]

# Profile Pictures
default_pfps = [
    "https://i.imgur.com/4M34hi2.png",  # PFP 1
    "https://i.imgur.com/0p6sszJ.png",  # PFP 2
    "https://i.imgur.com/ptL8WSc.jpeg",  # PFP 3
    "https://i.imgur.com/vVTymFO.jpeg",  # PFP 4
    "https://i.imgur.com/2NUN3xE.jpeg",  # PFP 5
    "https://i.imgur.com/H6HrHyL.jpeg",  # PFP 6
]

def print_ascii_art():
    ascii_art = """
   

▓█████▄  █     █░▓█████  ▄▄▄▄   
▒██▀ ██▌▓█░ █ ░█░▓█   ▀ ▓█████▄ 
░██   █▌▒█░ █ ░█ ▒███   ▒██▒ ▄██
░▓█▄   ▌░█░ █ ░█ ▒▓█  ▄ ▒██░█▀  
░▒████▓ ░░██▒██▓ ░▒████▒░▓█  ▀█▓
 ▒▒▓  ▒ ░ ▓░▒ ▒  ░░ ▒░ ░░▒▓███▀▒
 ░ ▒  ▒   ▒ ░ ░   ░ ░  ░▒░▒   ░ 
 ░ ░  ░   ░   ░     ░    ░    ░ 
   ░        ░       ░  ░ ░      
 ░                            ░ 
                                
    """
    gradient = ["\033[94m", "\033[96m", "\033[94m", "\033[94m"]
    for i, line in enumerate(ascii_art.splitlines()):
        gradient_color = gradient[i % len(gradient)]
        print(f"{gradient_color}{line}\033[0m")

 # Creators name
    print("\033[94mCreated by Zenusop\033[0m")

# Extra line of space
    print()

def generate_random_username(length=24):
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def validate_webhook_url(url):
    try:
        response = requests.get(url)
        # Check if the webhook URL is valid
        return response.status_code == 200
    except requests.RequestException:
        return False

def send_webhook(url, username=None, avatar_url=None, content=None, proxies=None):
    # Generate a random message if none is provided
    if content is None:
        content = random.choice(random_messages)
    
    # Prepare the payload for the request
    payload = {
        'username': username or generate_random_username(),
        'avatar_url': avatar_url or random.choice(default_pfps),
        'content': content
    }
    
    # Send the POST request to the webhook URL
    try:
        response = requests.post(url, json=payload, proxies=proxies)
        # Get the current timestamp for logging
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Handle the response
        if response.status_code == 204:
            print(f"\033[92m[+] [{timestamp}] Message sent successfully.\033[0m")
        elif response.status_code == 429:
            print(f"\033[91m[-] [{timestamp}] Rate limit exceeded. Try again later.\033[0m")
        else:
            print(f"\033[91m[-] [{timestamp}] Failed to send message. Status code: {response.status_code}\033[0m")
    except requests.RequestException as e:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"\033[91m[-] [{timestamp}] Error sending message: {e}\033[0m")

def main():
    print_ascii_art()
    
    webhooks = []
    
    while True:
        webhook_url = input("[+] Enter the Discord webhook URL: ").strip()
        if not webhook_url:
            if webhooks:
                break
            else:
                print("\033[91m[-] At least one webhook URL is required.\033[0m")
                continue
        
        if validate_webhook_url(webhook_url):
            webhooks.append(webhook_url)
            second_webhook = input("[+] Enter the second webhook URL (or press Enter to skip): ").strip()
            if second_webhook:
                if validate_webhook_url(second_webhook):
                    webhooks.append(second_webhook)
                else:
                    print("\033[91m[-] Invalid second webhook URL. Skipping...\033[0m")
            break
        else:
            print("\033[91m[-] Invalid webhook URL. Please check the URL and try again.\033[0m")
    
    proxy_input = input("[+] Enter proxy (e.g., http://username:password@proxyserver:port) or leave blank for no proxy: ").strip()
    proxies = None
    if proxy_input:
        proxies = {
            "http": proxy_input,
            "https": proxy_input
        }
    
    username = input("[+] Enter the username for the webhook (leave blank for random): ").strip() or None
    avatar_url = input("[+] Enter the URL for the profile picture (or leave blank for a random one): ").strip() or None
    custom_message = input("[+] Enter the custom message (leave blank for random): ").strip() or None
    delay_ms = int(input("[+] Enter the delay between messages in milliseconds (e.g., 1000): ").strip() or 1000)
    
    while True:
        for webhook_url in webhooks:
            send_webhook(webhook_url, username, avatar_url, custom_message, proxies)
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"\033[95m[+] [{timestamp}] Waiting {delay_ms / 1000} seconds before sending the next message...\033[0m")
            time.sleep(delay_ms / 1000)

if __name__ == "__main__":
    main()
