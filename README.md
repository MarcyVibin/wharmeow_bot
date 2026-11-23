<a id="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![License][license-shield]][license-url]

<h3 align="center">wharmeow_bot</h3>

<p align="center">
    A Discord bot for a community server: it welcomes newcomers with starter roles, hands out roles by reaction, translates messages and turns images into GIFs.
    <br />
    <br />
    <a href="https://github.com/MarcyVibin/wharmeow_bot/issues">Report Bug</a>
    &middot;
    <a href="https://github.com/MarcyVibin/wharmeow_bot/issues">Request Feature</a>
</p>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#requirements">Requirements</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

---

## About The Project

**wharmeow_bot** is a small [discord.py](https://github.com/Rapptz/discord.py) bot built for one community server. All server-specific IDs (guilds, roles, emojis, the reaction-role message) live in `constants.py`, so pointing it at another server only means editing that file.

Key features:

- Assigns newcomer roles automatically when a member joins a managed server
- Reaction roles: reacting to a configured message with a configured emoji grants the matching role
- `!translate`: reply to a message to get it translated into English
- `!make_gif` (aliases `!makegif`, `!gif`): turns an attached image into a GIF
- `/clear`: admin-only slash command that deletes messages in the current channel, or the last 14 days of one user's messages across the server
- `/help`: slash command that lists the commands
- Logs to `bot.log` next to the script
- Installs missing Python packages on first start

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

* [![Python][Python.org]][Python-url]
* [![discord.py][discordpy-badge]][discordpy-url]
* [![Pillow][Pillow-badge]][Pillow-url]
* [deep-translator](https://github.com/nidhaloff/deep-translator)
* [python-dotenv](https://github.com/theskumar/python-dotenv)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Getting Started

### Requirements

- Python 3.8+
- A Discord application with a bot token ([Discord Developer Portal](https://discord.com/developers/applications))
- The **Server Members** and **Message Content** privileged intents enabled for the bot in the portal. The bot reads joins, reactions and message content.
- `discord.py`, `deep-translator`, `python-dotenv` and `pillow`. The script installs them with `pip` on first start if they are missing.

### Installation

Clone the repository:

```sh
git clone https://github.com/MarcyVibin/wharmeow_bot.git
cd wharmeow_bot
```

Create a `.env` file next to `wharmeow_bot.pyw` with your bot token:

```sh
BOT_TOKEN=your-token-here
```

Then edit `constants.py` and replace the server, role, emoji, channel and message IDs with the ones from your own server.

---

## Usage

Start the bot:

```sh
python wharmeow_bot.pyw
```

On Windows you can also double-click `wharmeow_bot.pyw`, which runs it without a console window. Check `bot.log` for what the bot is doing.

| Command | Who | What it does |
| --- | --- | --- |
| `/help` | everyone | Lists the commands |
| `/clear [amount] [user]` | administrators | Deletes up to 100 messages in the channel, or the given user's messages from the last 14 days across the server |
| `!translate` | everyone | Reply to a message with this command to translate it to English |
| `!make_gif` | everyone | Attach an image (or reply to one) to get a GIF back |

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## License

Distributed under the GNU General Public License v3.0 (GPL-3.0). See `LICENSE` for more information.

---

## Contact

Marc Steger - marc.steger06@gmail.com

Project Link: https://github.com/MarcyVibin/wharmeow_bot

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Badge Links -->

[Python.org]: https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/

[discordpy-badge]: https://img.shields.io/badge/discord.py-Discord%20Bot-5865F2?style=for-the-badge&logo=discord&logoColor=white
[discordpy-url]: https://github.com/Rapptz/discord.py

[Pillow-badge]: https://img.shields.io/badge/Pillow-Imaging-blue?style=for-the-badge
[Pillow-url]: https://python-pillow.org/

[contributors-shield]: https://img.shields.io/github/contributors/MarcyVibin/wharmeow_bot.svg?style=for-the-badge
[contributors-url]: https://github.com/MarcyVibin/wharmeow_bot/graphs/contributors

[forks-shield]: https://img.shields.io/github/forks/MarcyVibin/wharmeow_bot.svg?style=for-the-badge
[forks-url]: https://github.com/MarcyVibin/wharmeow_bot/network/members

[stars-shield]: https://img.shields.io/github/stars/MarcyVibin/wharmeow_bot.svg?style=for-the-badge
[stars-url]: https://github.com/MarcyVibin/wharmeow_bot/stargazers

[issues-shield]: https://img.shields.io/github/issues/MarcyVibin/wharmeow_bot.svg?style=for-the-badge
[issues-url]: https://github.com/MarcyVibin/wharmeow_bot/issues

[license-shield]: https://img.shields.io/github/license/MarcyVibin/wharmeow_bot.svg?style=for-the-badge
[license-url]: https://github.com/MarcyVibin/wharmeow_bot/blob/main/LICENSE
