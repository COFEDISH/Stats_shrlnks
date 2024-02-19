from flask import Flask, render_template, request, redirect, render_template_string
import string
import socket
import json
import datetime
app = Flask(__name__)

subd_address = ("cofesubd-service.default.svc.cluster.local", 6379)
def get_current_date():
    today_date = datetime.datetime.today().strftime('%Y-%m-%d')
    return today_date

class ReportPrinter:

    def _print_structure(counts, depth=0, result=""):
        for key, value in counts.items():
            if isinstance(value, dict):
                sub_total = sum(value.values()) if isinstance(list(value.values())[0], int) else sum(
                    ReportPrinter._get_sub_totals(v) for v in value.values()
                )
                result += f"{' ' * depth}{key} {sub_total}\n"
                result = ReportPrinter._print_structure(value, depth=depth + 4, result=result)
            else:
                result += f"{' ' * depth}{key} {value}\n"
        return result

    def _get_sub_totals(sub_counts):
        if isinstance(list(sub_counts.values())[0], int):
            return sum(sub_counts.values())
        return sum(ReportPrinter._get_sub_totals(v) for v in sub_counts.values())


class DetailProcessor:
    def __init__(self, keys):
        self.keys = keys
        self.counts = {}

    def process_detail(self, data):
        for entry in data:
            curr_dict = self.counts
            for key in self.keys[:-1]:
                value = entry[key]
                curr_dict = curr_dict.setdefault(value, {})
            last_key = entry[self.keys[-1]]
            curr_dict.setdefault(last_key, 0)
            curr_dict[last_key] += 1

    def get_counts(self):
        return self.counts


@app.route('/', methods=['GET', 'POST'])
def get_report_structure():
    if request.method == 'POST':
        keys = [value for key, value in request.form.items()]

        date = get_current_date()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect(subd_address)
                s.sendall(f"efsd7ff8dsf --file data{date}.json --query 'GSON get'".encode())
                print("Message sent successfully.")
                datas_subd = s.recv(16384)
                data_sub = datas_subd.decode()
                print(data_sub)
            except ConnectionRefusedError:
                print("Connection to the server failed.")

        data_subs = json.loads(data_sub) if data_sub.strip() else {}
        data_subd = [entry for entry in data_subs if entry]

        processor = DetailProcessor(keys)
        processor.process_detail(data_subd)
        counts = processor.get_counts()

        report_result = ReportPrinter._print_structure(counts)
        print(report_result)
        return render_template('report.html', report=report_result)

    return render_template('index.html')  # Отображение формы ввода

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=50011, debug=True)
