# Introduction
**A Telegram Bot to force users to join a specific channel before sending messages in a group.**
- Find it on Telegram as [Force Subscriber](https://t.me/ForceSubscribeRoBot)

## Todo :
- [ ] Add multiple channels support
- [X] Configure different groups with different channels
- [ ] Clean messages after completion

## Deploy :

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)


### Installation :
- Clone this repo
```
git clone https://github.com/AmineSoukara/ForceSubscribeRobot.git
```
- Change directory
```
cd force-subscribe-telegram-bot
```
- Install requirements
```
pip3 install -r requirements.txt
```

### Configuration :
Add [APP_ID](https://my.telegram.org/apps), [API_HASH](https://my.telegram.org/apps), [BOT_TOKEN](https://t.me/botfather) in [Config.py](Config.py) or in Environment Variables.

### Deploying
- Run bot.py
```
python3 bot.py
```

## Thanks To :
- [PyroGram](https://PyroGram.org) & [Hasibul Kabir](https://GitHub.com/hasibulkabir) & [Spechide](https://GitHub.com/spechide) And [Adnan Ahmad](https://github.com/viperadnan-git)
