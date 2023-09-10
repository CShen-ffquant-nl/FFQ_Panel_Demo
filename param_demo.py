#param demo
#https://param.holoviz.org/user_guide/Dependencies_and_Watchers.html

import param

class C(param.Parameterized):
    _countries = {'Africa': ['Ghana', 'Togo', 'South Africa'],
                  'Asia'  : ['China', 'Thailand', 'Japan', 'Singapore'],
                  'Europe': ['Austria', 'Bulgaria', 'Greece', 'Switzerland']}
    
    continent = param.Selector(list(_countries.keys()), default='Asia')
    country = param.Selector(_countries['Asia'])
    
    @param.depends('continent', watch=True)
    def _update_countries(self):
        countries = self._countries[self.continent]
        self.param['country'].objects = countries
        if self.country not in countries:
            self.country = countries[0]

c = C()
print(f"{c.country}, {c.param.country.objects}")

c.continent='Africa'
print(f"{c.country}, {c.param.country.objects}")
