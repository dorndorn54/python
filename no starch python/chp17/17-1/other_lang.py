import requests
import pygal
from pygal.style import LightColorizedStyle as LCS, LightStyle as LS

# make api call and store the response
URL = 'https://api.github.com/search/repositories?q=language:C&sort=star'
r = requests.get(URL)
print("status:", r.status_code)

# store API response in variable
response_dict = r.json()
print("total repositories: ", response_dict['total_count'])

# explore info in the repos
repo_dicts = response_dict['items']

names, plot_dicts = [], []
for repo_dict in repo_dicts:
    names.append(repo_dict['name'])
    
    plot_dict = {
        'value': repo_dict['stargazers_count'],
        'label': repo_dict['description'],
        'xlink': repo_dict['html_url']
        }
    plot_dicts.append(plot_dict)

# make visualisation
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

chart = pygal.Bar(my_config, style=my_style)
chart.title = 'Most-Starred C Projects on GitHub'
chart.x_labels = names

chart.add('', plot_dicts)
chart.render_to_file('python_repos.svg')
