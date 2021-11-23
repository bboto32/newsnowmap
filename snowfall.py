from flask import Flask, request, render_template, jsonify
import total_snow as ts
from datetime import datetime, timedelta
import pytz
import os

app = Flask(__name__)

@app.route('/')
def my_func():
    return render_template('snowfall.html')

# TODO: timezone
# TODO: do not allow generate image above now()
@app.route('/get_total_snowfall', methods=['POST', 'GET'])
def get_total_snowfall():
    # get and process user input #
    start_date = request.form['start_date'].replace('-', '')
    start_hour = request.form['start_hour'].rjust(2, '0').ljust(4, '0')
    end_date = request.form['end_date'].replace('-', '')
    end_hour = request.form['end_hour'].rjust(2, '0')+'59'

    start_cet = pytz.timezone("Europe/Prague").localize(datetime.strptime(start_date+'.'+start_hour, '%Y%m%d.%H%M'))
    end_cet = pytz.timezone("Europe/Prague").localize(datetime.strptime(end_date+'.'+end_hour, '%Y%m%d.%H%M'))

    start = start_cet.astimezone(pytz.timezone("UTC"))
    end = end_cet.astimezone(pytz.timezone("UTC"))
    # timezone adjustment #
    # for request 10:00 - 12:59 CET I need data from 11, 12, 13 hour CET - that is 10, 11, 12 hour UTC #
    # for request 10:00 - 12:59 CEST I need data from 11, 12, 13 hour CEST - that is 9, 10, 11 hour UTC #

    # check if image exists otherwise create it #
    gen_img = os.listdir('./static')
    my_img_name = datetime.strftime(start, '%Y%m%d.%H%M') + '_' + datetime.strftime(end, '%Y%m%d.%H%M')
    if my_img_name+'.png' in gen_img:
        pass
    else:
        my_snow = ts.total_snow(start, end)
        my_img = ts.matrix_to_img(my_snow)
        ts.save_img(my_img, my_img_name + '.png')
        ts.save_legend(my_snow, my_img_name)

    return jsonify(start_dt=datetime.strftime(start.date(), '%d.%m.%Y'), start_hour=start_hour[:2]+':00',
                   end_dt=datetime.strftime(end.date(), '%d.%m.%Y'), end_hour=end_hour[:2]+':59',
                   img_name=my_img_name)

if __name__=='__main__':
    app.run(host='0.0.0.0')
