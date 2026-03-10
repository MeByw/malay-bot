import discord
from discord.ext import commands
from groq import AsyncGroq
from keep_alive import keep_alive
import os
from dotenv import load_dotenv

load_dotenv() # This loads your hidden .env keys!
# --- 1. SETUP AI ---
# 🚨 Insert your GROQ API key here (DO NOT SHARE IT ONLINE) 🚨
client = AsyncGroq(api_key="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")

# --- 2. SETUP DISCORD BOT ---
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# --- 3. THE TARGET USER ---
TARGET_USER_ID = 648056816176988161 

@bot.event
async def on_ready():
    print(f'AI Bot is online! Logged in as {bot.user}')

@bot.event
async def on_message(message):
    # Ignore the bot's own messages
    if message.author == bot.user:
        return

    # Check if someone @mentioned your bot in their message
    if bot.user in message.mentions:
        
        # Check if their message is a direct reply to another message
        if message.reference:
            replied_message = await message.channel.fetch_message(message.reference.message_id)
            
            # Check if that original message was written by your TARGET_USER
            if replied_message.author.id == TARGET_USER_ID:
                print(f"Target located! Reading message: '{replied_message.content}'")
                
                prompt = f"Someone said: '{replied_message.content}'. Please respond by giving them helpful, friendly advice in one simple sentence in Classical Malay Language."
                
                try:
                    # Ask Groq to generate the response using Meta's Llama 3 model
                    chat_completion = await client.chat.completions.create(
                        messages=[
                            {
                                "role": "user",
                                "content": prompt,
                            }
                        ],
                        model="llama-3.3-70b-versatile", # Super fast and smart free model
                    )
                    
                    # Extract the text from Groq's response
                    reply_text = chat_completion.choices[0].message.content
                    
                    await replied_message.reply(reply_text)
                    print("AI response sent successfully!")
                    
                except Exception as e:
                    print(f"AI Error: {e}")
                    # Changed your error message to fit the Classical Malay theme!
                    await message.channel.send("Minda hamba sedikit celaru sekarang. Cubalah sebentar lagi!")

    await bot.process_commands(message)

# Start the background web server to keep the bot alive
keep_alive()

# 🚨 Run the bot using the secret token from your .env vault
bot.run(os.getenv('DISCORD_TOKEN'))
# 🚨 Insert your NEW Discord Token here (DO NOT SHARE IT ONLINE) 🚨
bot.run('MTQ4MDk0NDgyMTEzNTczNjk3Mw.GtzGo5.FQ7NaOYDkhe8d4iF4N9AOjLyxoKKQ78aBac80k')