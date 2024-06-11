# Grizzly Sms
##### **grizzlysms** - this is a simple and modern platform for the Grizzly SMS API, written in Python 3.8+ using requests.

So far, does not support rental, only activation.

## quick start
Installation
Clone library to your project
```
git clone https://github.com/giwih/grizzlysms.git
```
Import librarry
```python
from grizzly import Grizzly

grizzly = Grizzly(api_key="your api key")
```
you can take the api key from https://grizzlysms.com/profile/settings (or grizzlysms1.com for Russia)
##### usage
```python
from grizzly import Grizzly

grizzly = Grizzly(api_key="your api key")
balance = grizzly.get_balance()
costnumber = grizzly.get_cost('go', '7') #the first argument is the id of the service, the second country. You can get all id services/countres from here
countnumbers = grizzly.get_count('go', '7')

print(f"""
Your balance: {balance}
Cost number: {costnumber}
Count numbers: {countnumbers}""")
```
## more details here - https://github.com/giwih/grizzlysms/wiki
#### You can get all id services/countres from [here](https://github.com/giwih/grizzlysms/blob/master/codes.md)

##### Number
```python
#get number
number = grizzly.get_number('go', '7') #returns the activation ID:Number
print(number) # 123456:601234567890; 123456- activation ID; 601234567890 - phone number

#get code
code = grizzly.get_code('95972496') #the argument - your activation ID
"""
get_code() can return several statuses:
STATUS_WAIT_CODE - waiting for SMS
STATUS_CANCEL - activation canceled
STATUS_OK:$code - the code was received (where $code is the activation code)
"""
#change status
status = grizzly.change_status('96005647', '-1') #the first argument is the activation ID, second - activation status.  
"""
All activation statuses:
-1 — cancel activation
1 — inform about the readiness of the number (sms sent to the number);
3 — wait for the next code on the same number;
6 — complete activation;
8 — cancel activation.

change_status() can return several statuses:
ACCESS_READY — the availability of the room has been confirmed;
ACCESS_RETRY_GET — waiting for a new SMS;
ACCESS_ACTIVATION — the service has been successfully activated;
ACCESS_CANCEL — activation has been canceled.
"""
```
## Tasks:
- [x] Basic Library
- [x] Github wiki
- [ ] Publication on PyPiP
- [ ] Creating documentation
- [ ] Room rental support
- [ ] Loggining