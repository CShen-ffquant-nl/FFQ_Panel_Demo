#param demo - without class then dependency is not working
#https://param.holoviz.org/user_guide/Dependencies_and_Watchers.html

import param

_countries = {'Africa': ['Ghana', 'Togo', 'South Africa'],
                'Asia'  : ['China', 'Thailand', 'Japan', 'Singapore'],
                'Europe': ['Austria', 'Bulgaria', 'Greece', 'Switzerland']}

continent = param.Selector(list(_countries.keys()), default='Asia')
country = param.Selector(_countries['Asia'])

@param.depends('continent', watch=True)
def _update_countries():
    countries = _countries[continent]
    param['country'].objects = countries
    if country not in countries:
        country = countries[0]

print(f"{country}, {country.objects}")

continent='Africa'
print(f"{country}, {country.objects}")
