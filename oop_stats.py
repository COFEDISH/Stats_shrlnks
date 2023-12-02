from flask import Flask, render_template, request, redirect, render_template_string
import string
import socket
import json
import datetime
app = Flask(__name__)


subd_address = ('37.193.53.6', 6379)
def get_current_date():
    today_date = datetime.datetime.today().strftime('%Y-%m-%d')
    return today_date


class Counter:
    def __init__(self, data):
        self.data = data
        self.counts = {}
        print(data)

    def count_parameters(self, string1, string2, string3):
        print(string1, string2, string3)
        for entry in self.data:
            if string1 in entry and string2 in entry and string3 in entry:
                entry1 = entry[string1]
                entry2 = entry[string2]
                entry3 = entry[string3]

                self.counts.setdefault(entry1, {})
                self.counts[entry1].setdefault(entry2, {})
                self.counts[entry1][entry2].setdefault(entry3, 0)
                self.counts[entry1][entry2][entry3] += 1
        print(self.counts)

    def get_counts(self):
        return self.counts



class Report:
    def generate_report(counter):
        counts = counter.get_counts()

        formatted_report = ""
        for string1, string2 in counts.items():
            formatted_report += f"{string1} {sum(sum(string3.values()) for string3 in string2.values())}\n"
            for string3, count in string2.items():
                formatted_report += f"    {string3} {sum(count.values())}\n"
                for key, value in count.items():
                    formatted_report += f"        {key} {value}\n"

        return formatted_report


@app.route('/', methods=['GET', 'POST'])
def get_report_structure():
    if request.method == 'POST':

        string1 = request.form['param1']
        string2 = request.form['param2']
        string3 = request.form['param3']

        print(string1, string2, string3)

        date = get_current_date()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect(subd_address)
                s.sendall(f"--file data{date}.json --query 'GSON get'".encode())
                print("Message sent successfully.")
                datas_subd = s.recv(16384)
                data_sub = datas_subd.decode()
                print(data_sub)
            except ConnectionRefusedError:
                print("Connection to the server failed.")
        data_subd = json.loads(data_sub)
        counter = Counter(data_subd)
        print(counter.count_parameters(string1, string2, string3))


        report = Report.generate_report(counter)
        print(report)
        return render_template('report.html', report=report)  # Отображение шаблона с отчетом

    return render_template('index.html')  # Отображение формы ввода


if __name__ == '__main__':
    app.run(host='192.168.0.105', port=50011, debug=True)