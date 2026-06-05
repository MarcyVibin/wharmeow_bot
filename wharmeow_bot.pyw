import sys
import subprocess
import os
from pathlib import Path
import logging

REQUIREMENTS = {
  "deep-translator": "deep_translator",
  "discord.py": "discord",
  "python-dotenv": "dotenv",
  "pillow": "pillow"
}

log_file = Path(sys.argv[0]).resolve().parent / "bot.log"
logging.basicConfig(
  filename=log_file,                                       # log file path
  level=logging.INFO,                                      # minimum level to capture
  filemode="a",                                            # append to existing log
  format="%(asctime)s [%(levelname)s] %(message)s"
)

def ensure_dependencies():
  for pip_name, import_name in REQUIREMENTS.items():
    try:
      __import__(import_name)
    except ImportError:
      print(f"Installing {pip_name}...")
      subprocess.check_call([
        sys.executable, "-m", "pip", "install", pip_name
      ])
ensure_dependencies()

try:
  from deep_translator import GoogleTranslator
  from PIL import Image
  from io import BytesIO
  import constants
  from dotenv import load_dotenv
  import discord
  from discord import app_commands
  from discord.ext import commands
except:
  print("Error when importing packages.")




intents = discord.Intents.default()
intents.messages = True
intents.members = True
intents.reactions = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)



#==========================================
# Helper functions
#==========================================
def convertToGif(image: Image.Image, duration: int = 100, loop: int = 0) -> BytesIO:
  frame = image.convert("RGB").quantize(colors=256,
                                        method=Image.MEDIANCUT,
                                        dither=Image.FLOYDSTEINBERG)

  buffer = BytesIO()
  frame.save(buffer,
              format="GIF",
              save_all=False,  # single frame
              duration=duration,
              loop=loop,
              optimize=False)
  buffer.seek(0)
  return buffer

async def add_role(member: discord.Member):
  for role_id in constants.NEWCOMER_ROLES:
    role = member.guild.get_role(role_id)
    if role:
      await member.add_roles(role)
      logging.info(f"Assigned role '{role.name}' (ID: {role.id}) to new member {member.name}#{member.discriminator} (ID: {member.id})")
    else:
      logging.warning(f"Role ID {role_id} not found in guild {member.guild.name} (ID: {member.guild.id})")


#==========================================
# Command Functions
#==========================================
@bot.tree.command(name="help", description="Lists commands.")
async def hello(interaction: discord.Interaction):
  logging.info(f"Help command used by {interaction.user} in guild {interaction.guild}.")
  await interaction.response.send_message("use !make_gif or !makegif to convert an image into a gif.")

@bot.tree.command(name="clear", description="Clear messages from this channel")
@commands.has_permissions(administrator=True)
async def clear(interaction: discord.Interaction, amount: app_commands.Range[int, 1, 100] = 1):
  await interaction.response.defer(thinking=False)
  await interaction.channel.purge(limit=amount + 1)

@bot.command(name="translate", help="Translate the replied message to English.")
async def translate(ctx: commands.Context):
  if ctx.message.reference is None:
    await ctx.send("Reply to a message and use this command.")
    return

  try:
    referenced_message = await ctx.channel.fetch_message(
      ctx.message.reference.message_id
    )

    original_text = referenced_message.content

    if not original_text:
      await ctx.send("The referenced message contains no text.")
      return

    translated = GoogleTranslator(
      source="auto",
      target="en"
    ).translate(original_text)

    await ctx.send(
      f"**Translation:**\n{translated}"
    )

  except Exception as e:
    await ctx.send(f"Translation failed: {e}")

@bot.command(name="make_gif", help="Turn an attached image into a GIF", aliases=["makegif", "gif"])
async def make_gif(ctx: commands.Context):
  # Case 1: Check for attachments in the command message
  if ctx.message.attachments:
    images = ctx.message.attachments

  # Case 2: Check if the command is a reply to a message
  elif ctx.message.reference:
    replied_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
    if replied_message.attachments:
      images = replied_message.attachments

  # If no images found
  if not images:
    await ctx.send("Please attach an image or reply to a message containing an image.")
    return

  gif_files = []
  for image in images:

    # Download and open the image
    img_bytes = await image.read()

    bio = BytesIO(img_bytes)
    gif_bytes: BytesIO
    with Image.open(bio) as pil_image:
      gif_bytes = convertToGif(pil_image)
    del bio
    gif_files.append(discord.File(fp=gif_bytes, filename="marcybot.gif"))

  logging.info(f"Converted {len(gif_files)} image(s) to GIF for user {ctx.author} in guild {ctx.guild}.")
  await ctx.send("Heres your gif(s).", files=gif_files)

  for f in gif_files:
    f.close()   # free memory
  gif_files.clear()

  return


#==========================================
# Event Functions
#==========================================
@bot.event
async def on_ready():
  guild = discord.Object(id=constants.CAT_SERVER_ID)

  # sync only for this guild
  await bot.tree.sync(guild=guild)
  logging.info(f"Commands synced to test guild {guild.id}")

  # optional: global sync (cached, takes ~1 hour to update)
  await bot.tree.sync()
  logging.info("Global commands synced (may take up to an hour to propagate)")

  discord.Activity(type=discord.ActivityType.playing, name="/help")

  logging.info(f"Logged in as {bot.user}")

@bot.event
async def on_member_join(member: discord.Member):
  if member.guild.id in constants.MANAGED_GUILDS:
    await add_role(member)
    logging.info(f"New member {member.name}#{member.discriminator} (ID: {member.id}) joined guild {member.guild.name} (ID: {member.guild.id}). Assigning newcomer roles.")

@bot.event
async def on_member_remove(member: discord.Member):
  if member.guild.id in constants.MANAGED_GUILDS:
    logging.info(f"Member {member.name}#{member.discriminator} (ID: {member.id}) left guild {member.guild.name} (ID: {member.guild.id}).")

@bot.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
  if payload.user_id == bot.user.id:
    return

  channel_map = constants.REACTION_ROLES.get(payload.channel_id)
  if not channel_map:
    return

  message_map = channel_map.get(payload.message_id)
  if not message_map:
    return

  role_id = message_map.get(payload.emoji.id)
  if not role_id:
    return

  guild = bot.get_guild(payload.guild_id)
  member = guild.get_member(payload.user_id) or await guild.fetch_member(payload.user_id)

  role = guild.get_role(role_id)
  if role:
    await member.add_roles(role)


load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
bot.run(TOKEN)
