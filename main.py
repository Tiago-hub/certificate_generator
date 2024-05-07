import sys
from pathlib import Path
import json
import argparse
import csv

file_path = Path(__file__)
dir_path = file_path.parent

from resources import Certificate
from resources import CustomMail

def load_config():
    with open("./config.json") as conf_file:
        configs = json.load(conf_file)
        return configs

# certificate = Certificate("../Templates/template-gefel.png", "../Fonts/PoetsenOne-Regular.ttf", vertical_offset=(-550)) 
# with certificate as cert:
#     cert.generate_certificate("tiagof")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", dest="model", help="The model defined in config.json")
    parser.add_argument("--csv", dest="csv", help="The csv file with a collumn with 'nomes/name'")
    parser.add_argument("--date", dest="date_lec", help="The date of the lecture")
    parser.add_argument("--title", dest="title_lec", help="The title of lecture")
    parser.add_argument("--lecturer", dest="lecturer", help="The name of lecturer")
    args = parser.parse_args()

    configs = load_config()
    config = configs.get(args.model)
    lec_date = "" if args.date_lec is None else args.date_lec
    lec_title = "" if args.title_lec is None else args.title_lec
    lecturer = "" if args.lecturer is None else args.lecturer
    if config is None:
        print("[ERROR] Invalid model supplied. Please check/add a valid model in config.json file")
        sys.exit(1)
    if not Path(args.csv).exists():
        print("[ERROR] The path to csv file does not exists")
        sys.exit(1)
    csv_file = Path(args.csv)
    certificate = Path(dir_path/config.get("certificate"))
    font = Path(dir_path/config.get("font"))
    h_offset = config.get("h_offset")
    v_offset = config.get("v_offset")
    email_details = config.get("email_details")
    email_subject = email_details.get("subject")
    email_body = email_details.get("body")
    sender_email = config.get("sender_email")
    sender_password = config.get("sender_app_password")

    certificate = Certificate(certificate, font, vertical_offset=v_offset) 

    name_list = []
    email_dict = {}
    with csv_file.open() as csvfile:
        name_col = None
        email_col = None
        for line in csv.reader(csvfile):
            if name_col is None or email_col is None:
                for index, col in enumerate(line):
                    if "name" in col.lower() or "nome" in col.lower():
                        name_col = index
                    elif "email" == col.lower():
                        email_col = index
          
            else:
                name = line[name_col]
                email = line[email_col]
                name_list.append(name)
                email_dict[name] = email

    name_list.sort()
    certs_dict = {}
    for name in name_list:
        with certificate as cert:
            cert_path = cert.generate_certificate(name, f"{name}_certificado_gefel")
            certs_dict[name] = cert_path

    with CustomMail(sender_email, sender_password) as mail:
        for name, cert in certs_dict.items():
            email = email_dict[name]
            print(f"Sending to {name} in email {email} the cert in {cert}")
            subject = email_subject.format(lec_title=lec_title, lec_date=lec_date)
            body = email_body.format(lec_date=lec_date, lec_title=lec_title, lecturer=lecturer)
            mail.send_mail(email, f"Certificado - {lec_title}", body, cert)
