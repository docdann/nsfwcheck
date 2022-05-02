import http.client
import os
import re

from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/')
def my_form():
    return render_template('my-form.html')


@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    processed_text = text.upper()
    return processed_text


@app.route('/nsfw')
def nsfw_form():
    return render_template('my-form.html')


@app.route('/nsfw', methods=['POST'])
def nsfw():  # see nsfw.py
    searchurl = request.form['text']
    print(searchurl)
    conn = http.client.HTTPSConnection("nsfw3.p.rapidapi.com")

    payload = "url=" + str(searchurl)

    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'X-RapidAPI-Host': "nsfw3.p.rapidapi.com",
        'X-RapidAPI-Key': os.environ['RAPIDAPI_KEY']
    }
    conn.request("POST", "/v1/results", payload, headers)

    res = conn.getresponse()
    data = res.read()
    nsfw_value = data.decode("utf-8")
    pattern1 = re.compile(r'"nsfw":0.\d+')
    matches = pattern1.finditer(nsfw_value)
    for match in matches:
        nsfw_value_segment = match.group(0)
        nsfw_seg_value = re.sub(r'"nsfw":', "", nsfw_value_segment)
        print(nsfw_seg_value)
        if float(nsfw_seg_value) < 0.8:
            print("This media is SFW")

            return '''<head> 
                <meta charset="UTF-8">
              <title>NSFW RESULTS</title>
               </head>
               <body>Percent NSFW : {} This media is SFW!</body><img src= {} alt="Italian Trulli"/>'''.format(nsfw_seg_value, searchurl)
        else:
            # print(type(data))
            # print(data.decode("utf-8"))
            return '''<head> 
            <meta charset="UTF-8">
          <title>NSFW RESULTS</title>
           </head>
           <body>Percent NSFW : {} This media is NSFW!</body>'''.format(nsfw_seg_value)
            # results need to be passed to html


if __name__ == '__main__':
    app.run()