
# from __future__ import print_function
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt, mpld3
df = plt.plot([1,2,3],[4,6,5])
plt.show()

print('Heres some data1')
print('Other important')
print('I AM DATA CARE ABOUT ME')
print('guyss im important its me data')
myfig = plt.figure(1)
sales_report= plt.plot([1,9,10],[1,7, 10], c = 'g')
plt.show()

# I will practice with generating a markdown file from python in here
from jinja2 import Environment, FileSystemLoader
import weasyprint
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template("myreport.html")

# creat the template variables dictionary
template_vars = {"title" : "My title in the dict yay",
                 "html_fig": mpld3.fig_to_html(myfig)}

mpld3.save_html(myfig, 'fig.html')

html_out = template.render(template_vars)

with open("practice.html", "w") as fh:
    fh.write(html_out)

# Trying xhtml2pdf
from xhtml2pdf import pisa

pdf = pisa.CreatePDF(html_out,open('report.pdf', 'wb'))

template.close()





# from weasyprint import HTML
# HTML('practice.html').write_pdf('report.pdf') # Same as …
