from flask import Flask, render_template, request
import re

from sympy import count_ops

app = Flask(__name__)

@app.route('/')

def home_fun():
    return render_template('homepage.html')


@app.route('/search')
def search_fun():
    x = request.args['in_1']
    y = str(request.args['in_2'])
    counter = 0
    # pattern = re.compile(x)
    res = []
    for i in re.finditer(r"{}".format(x),y):
        counter +=1
        strn = "Match {} \"{}\" : starts at {} and ends at {}".format(counter,i.group(),i.start(),i.end())
        res.append(strn)

    # out_start= list()
    # out_end  = list()
    # out_group = list()
    # for i in results:
    #     out_group.append(i.group())
    #     out_start.append(i.start())
    #     out_end.append(i.end())

    if counter>0:
            return render_template('searchresult.html', sub_str = x, main_str = y, result = res)
        
    else:
        return('Please enter correct pattern')

if __name__=='__main__':
    app.run(debug=True)