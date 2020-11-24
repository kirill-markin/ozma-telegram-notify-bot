# NotifBot
## Packages used
- Python 3.7.0 64bit
- telegram
- python-telegram-bot
- oauthlib
- requests_oauthlib

## Configuration
### [config.json](config.json)
- token: your tg bot token
- bot_notification_time: time of the day (like "07:00:00") to send the notification
- bot_update_time: time (in seconds) to pass between token renewals and time checks
- db_address: database API URL
- db_username: database username
- db_password: database password
- db_client_id: API access app name
- db_client_secret: API access secret
- db_view_name: View name to get data from
- db_schema_name: View schema name
- notification_list: List of people to notify (in JSON format)

### notification [list.json](list.json)
An array of entries with following fields:
- tg_id: User's Telegram ID (int, default value is -1)
- tg_username: User's Telegram username (like "kirmark") (string, default value is empty)
- chat_id: Chat ID associated with the user, this will be written down by the bot itself
- phone: !Dose not work now. User's phone, but it's not used right now due to how Telegram chooses to show phone numbers (string, default value is "None")

## Launching
Just use your Python on main.py.