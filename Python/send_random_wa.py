# pip install pywhatkit
import pywhatkit, random, string, time

group_id = ""
n = 30
letters = string.ascii_lowercase

for _ in range(n):
    k = random.randint(20, 50)
    s = ''.join(random.choice(letters) for _ in range(k))
    pywhatkit.sendwhatmsg_to_group_instantly(group_id, s, tab_close=True, close_time=1)
    time.sleep(1)