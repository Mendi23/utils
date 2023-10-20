import pandas as pd
import pywhatkit as kit
from datetime import datetime
import time, pathlib

# --- monkey-patching the "send_message" function
# --- See this PR: https://github.com/Ankit404butfound/PyWhatKit/pull/291/
from pywhatkit.core import core
import pyperclip
def send_message(message: str, receiver: str, wait_time: int) -> None:
    """Parses and Sends the Message"""
    core._web(receiver=receiver, message=message)
    time.sleep(7)
    core.click(core.WIDTH / 2, core.HEIGHT / 2)
    time.sleep(wait_time - 7)
    if not core.check_number(number=receiver):
        pyperclip.copy(message)
        core.hotkey("ctrl","v")
    core.press("enter")
core.send_message = send_message


def load_file(fp) -> pd.DataFrame:
    df = pd.read_csv(file_path, header=0,
                 converters={'time': lambda s: datetime.strptime(s, '%H:%M').time()},
                 )
    df['last_send'] = datetime.fromtimestamp(0).date()
    return df

def send_whatsapp_msg(group_id: str, message: str):
    kit.sendwhatmsg_to_group_instantly(group_id, message,
                                        wait_time=10,
                                        close_time=2,
                                        tab_close=True)

def send_messages(df: pd.DataFrame):
    current_dt = datetime.now()
    current_date = current_dt.date()
    for idx, row in df.iterrows():
        try:
            group_id = row['id']
            if current_date > row['last_send'] and current_dt.time() >= row['time']:
                send_whatsapp_msg(group_id, row['message'])
                print(f"Message sent to {group_id}")
        except Exception as e:
            print(f"Failed to send message to {group_id}: {e}")
        finally:
            df.at[idx, 'last_send'] = current_date


if __name__ == "__main__":
    file_path = pathlib.Path(__file__).parent.absolute() / "groups.csv"
    df = load_file(file_path)
    while True:
        send_messages(df)
        time.sleep(60)