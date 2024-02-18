import pandas as pd
import panel as pn
import hvplot as hv
from datetime import datetime
from datetime import date,timedelta
pn.extension('bokeh', template='bootstrap')
import hvplot.pandas

@pn.cache
def get_df(todaydate):
    todaydate2 = datetime.today().strftime("%Y-%m-%d")
    # todaydate2 =todaydate.strftime("%Y-%m-%d")
    url = f"https://raw.githubusercontent.com/alirezax2/GurusFocusCrawl/main/gurufocus/GuruFocus_merged_{todaydate2}.csv"
    df = pd.read_csv(url)
    
    return df

todaydate = pn.widgets.DatePicker(
    name ="End Date",# value=datetime(2000, 1, 1),
    description='Select a Date',
    end= date.today() #date(2023, 9, 1)
)

todaydate2 = datetime.today().strftime("%Y-%m-%d")   
df = get_df(todaydate2)
selectedcol = pn.widgets.Select(name='Select Ratio', value = 'PEG Ratio', options=list(df.columns))
selecteditem = pn.widgets.Select(name='Select Item', options=['Industry' , 'Sector'])
selectedmethod = pn.widgets.Select(name='Select Method', value= 'Mean' , options=['Mean', 'Min' , 'Max'])

selectedhover = 'Ticker'
hv.extension('bokeh')

def create_plot(selectedcol,selecteditem,todaydate,selectedmethod):
    df = get_df(todaydate)
    if selectedmethod=='Mean':
        group_means = df.groupby(selecteditem)[selectedcol].mean()
    if selectedmethod=='Min':
        group_means = df.groupby(selecteditem)[selectedcol].min()
    if selectedmethod=='Max':
        group_means = df.groupby(selecteditem)[selectedcol].max()
    df2 = df.merge(group_means, left_on=selecteditem, right_index=True, suffixes=('', f'_{selecteditem}_{selectedmethod}'))

    return df2.hvplot.bar(x=selecteditem, y=f'{selectedcol}_{selecteditem}_mean', hover_cols=selectedhover, height=800, width=1800).opts(xrotation=90, fontsize={'xticks': 10})

bound_plot = pn.bind(create_plot, selectedcol=selectedcol , selecteditem=selecteditem, todaydate=todaydate, selectedmethod=selectedmethod)
pn.Column(pn.Row(selectedcol, selecteditem, todaydate,selectedmethod), bound_plot).servable(title="Financial Sector Ratios Navigator")


