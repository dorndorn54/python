# using data from hn_submission.py to show most active discussions
# submission title and hyperlink should be included

import requests
import pygal
from pygal.style import LightColorizedStyle as LCS, LightStyle as LS
from operator import itemgetter

# make the api call and store repsonse
URL = 'https://hacker-news.firebaseio.com/v0/topstories.json'
r = requests.get(URL)
print("status code: ", r.status_code)

# explore the info in the repos
sub_ids = r.json()
sub_dicts = []
for sub_id in sub_ids[:30]:
    # make a separate api call for each
    url = ('https://hacker-news.firebaseio.com/v0/item/' + str(sub_id) + '.json')
    sub_r = requests.get(url)
    print(sub_r.status_code)
    response_dict = sub_r.json()

    sub_dict = {
        'title': response_dict['title'],
        'link': 'http://news.ycombinator.com/item?id=' + str(sub_id),
        'comments': response_dict.get('descendants', 0)
        }
    sub_dicts.append(sub_dict)

sub_dicts = sorted(sub_dicts, key=itemgetter('comments'), reverse=True)

# creating the x and y values
titles, plot_dicts = [], []
for sub_dict in sub_dicts:
    titles.append(sub_dict['title'])

    plot_dict = {
        'value': sub_dict['comments'], # must use the key words value and label and xlink for the plot
        'label': sub_dict['title'],
        'xlink': sub_dict['link']
        }
    plot_dicts.append(plot_dict)


print(titles)
print(plot_dicts)

# Make visualization.
my_style = LS()
my_config = pygal.Config()
my_config.x_label_rotation = 45
my_config.show_legend = False
my_config.title_font_size = 24
my_config.label_font_size = 14
my_config.major_label_font_size = 18
my_config.truncate_label = 15
my_config.show_y_guides = False
my_config.width = 1000
my_config.y_title = 'number of comments'

chart = pygal.Bar(my_config, style=my_style)
chart.title = 'H-news data'
chart.x_labels = titles

chart.add('', plot_dicts)
chart.render_to_file('Hnews_repos.svg')
