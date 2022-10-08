from typing import Dict
import pywhatkit, csv, pathlib


image_path = pathlib.Path(__file__).parent.absolute() / "invite.png"
msg = "נשמח לראותכם, מנדי וליאל❤️"
# msg = "ועכשיו עם הקובץ"

def transform_phone(x):
    canonized = '+' + "".join(filter(str.isdigit, x))
    if len(canonized) == 13 and canonized.startswith("+972"):
        return canonized
    else:
        raise ValueError("wrong number") 

def write_dict_as_csv(d: Dict, fp: str):
    with open(fp, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quotechar='"')
        writer.writerows(d.items())

def send_invites(fp):
    with open(fp, newline='') as csv_file:
        reader = csv.reader(csv_file, delimiter=',', quotechar='"')
        for name, phone in reader:
            try:
                pywhatkit.sendwhats_image(phone, image_path, msg, 8, True)
            except Exception as e:
                print(f'Error: {name=}, {phone=}, {e}')


def extract_invitee_list():
    
    csv_path = pathlib.Path(__file__).parent.absolute() / "invite_list.csv"
    fieldnames=['name', 'how', 'side', 'phone', 'group']
    mendi_invitees, liel_invitees = {}, {}

    with open(csv_path, newline='') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',', quotechar='|')
        for row in reader:
            d = {key: row[key] for key in fieldnames}
            if d['how'] == '':
                try:
                    canonized = transform_phone(d['phone'])
                except ValueError:
                    print(f"{d['side']}, {d['phone']}, {d['name']}, illegal combo")
                else:
                    tmp_d = mendi_invitees if d['side']== '' else liel_invitees
                    tmp_d[d['name']] = canonized
    write_dict_as_csv(mendi_invitees, 'mendis.csv')
    write_dict_as_csv(liel_invitees, 'liels.csv')
    
if __name__ == "__main__":
    extract_invitee_list()
