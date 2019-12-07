 # Copyright Google Inc. 2017
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import concurrent
import time
import numpy as np
import pandas as pd
import csv
from pandas.compat import StringIO
from bokeh.plotting import figure
from bokeh.io import show, curdoc
from bokeh.models import ColumnDataSource, CDSView, GroupFilter
from bokeh.models import LinearAxis, Range1d
from bokeh.models import Span
from bokeh.models import HoverTool
from bokeh.models.widgets import Tabs,Panel

# Hide some noisy warnings
logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)


def modify_doc(doc):
    csvdata = StringIO("""ind,Team1,is_batting_team,innings_over,innings_score,innings_wickets,score_target,total_runs,predictions
    0,Chennai Super Kings,1,1_1,6,0,-1,6,0.288274169
    1,Chennai Super Kings,1,1_2,12,0,-1,6,0.301675141
    2,Chennai Super Kings,1,1_3,16,0,-1,4,0.281522751
    3,Chennai Super Kings,1,1_4,29,0,-1,13,0.357313812
    4,Chennai Super Kings,1,1_5,39,0,-1,10,0.270430624
    5,Chennai Super Kings,1,1_6,42,1,-1,3,0.236661002
    6,Chennai Super Kings,1,1_7,51,1,-1,9,0.638245642
    7,Chennai Super Kings,1,1_8,57,1,-1,6,0.61583519
    8,Chennai Super Kings,1,1_9,64,2,-1,7,0.427738696
    9,Chennai Super Kings,1,1_10,75,2,-1,11,0.562660575
    10,Chennai Super Kings,1,1_11,77,2,-1,2,0.298964292
    11,Chennai Super Kings,1,1_12,87,2,-1,10,0.557578444
    12,Chennai Super Kings,1,1_13,97,3,-1,10,0.518214703
    13,Chennai Super Kings,1,1_14,109,3,-1,12,0.483040333
    14,Chennai Super Kings,1,1_15,117,3,-1,8,0.49632439
    15,Chennai Super Kings,1,1_16,127,3,-1,10,0.486246377
    16,Chennai Super Kings,1,1_17,130,4,-1,3,0.271725684
    17,Chennai Super Kings,1,1_18,139,4,-1,9,0.379939169
    18,Chennai Super Kings,1,1_19,148,4,-1,9,0.340993494
    19,Chennai Super Kings,1,1_20,163,5,-1,15,0.190012038
    20,Chennai Super Kings,0,2_1,2,0,163,2,0.09407036
    21,Chennai Super Kings,0,2_2,14,0,163,12,0.038120814
    22,Chennai Super Kings,0,2_3,19,0,163,5,0.037553594
    23,Chennai Super Kings,0,2_4,27,1,163,8,0.03882841
    24,Chennai Super Kings,0,2_5,36,1,163,9,0.039770603
    25,Chennai Super Kings,0,2_6,41,1,163,5,0.038807716
    26,Chennai Super Kings,0,2_7,44,3,163,3,0.053214338
    27,Chennai Super Kings,0,2_8,51,3,163,7,0.049129184
    28,Chennai Super Kings,0,2_9,61,3,163,10,0.03820334
    29,Chennai Super Kings,0,2_10,75,3,163,14,0.043611407
    30,Chennai Super Kings,0,2_11,80,3,163,5,0.036478572
    31,Chennai Super Kings,0,2_12,87,3,163,7,0.040550984
    32,Chennai Super Kings,0,2_13,102,3,163,15,0.053241987
    33,Chennai Super Kings,0,2_14,107,3,163,5,0.043090712
    34,Chennai Super Kings,0,2_15,112,4,163,5,0.059327953
    35,Chennai Super Kings,0,2_16,125,4,163,13,0.039308213
    36,Chennai Super Kings,0,2_17,139,5,163,14,0.018231714
    37,Chennai Super Kings,0,2_18,146,7,163,7,0.026232569
    38,Chennai Super Kings,0,2_19,156,7,163,10,0.014671202
    39,Chennai Super Kings,0,2_20,164,7,163,8,1""")

    df = pd.read_csv(csvdata, sep=",")
    df = df.set_index(['ind'])


    over=list(df.innings_over)
    score=list(df.innings_score)
    pred=list(df.predictions)
    color_innings=['blue']*20 + ['red']*20

    df['color_innings']=df.apply(lambda x:'Blue' if x['is_batting_team']==1 else 'Red',axis=1)
    df['color_innings']=df.apply(lambda x:'Blue' if x['is_batting_team']==1 else 'Red',axis=1)

    select_tools=['box_select', 'lasso_select', 'poly_select', 'tap', 'reset','hover','wheel_zoom']
    fig_hover=[('Team','@Team1'),('Total runs','@score')]

    df_cdf=ColumnDataSource(df)

    view_cdf_1=CDSView(source=df_cdf,filters=[GroupFilter(column_name='is_batting_team',group='1')])
    view_cdf_2=CDSView(source=df_cdf,filters=[GroupFilter(column_name='is_batting_team',group='0')])

    fig_list=figure(x_range=over,plot_height=500,plot_width=1000,tools=select_tools,tooltips=[('Team','@Team1'),('Innings Score','@innings_score')])
        
    fig_list.extra_y_ranges={"foo":Range1d(start=0,end=1)}
    fig_list.add_layout(LinearAxis(y_range_name='foo'),'right')
    fig_list.y_range.start=0

    fig_list.vbar(x='innings_over',top='total_runs',source=df_cdf,width=0.9,color='color_innings',legend='Score')

    fig_list.line(x='innings_over',y='predictions',source=df_cdf,color='green',y_range_name='foo',legend='Prediction Trend')
    fig_list.circle(x='innings_over',y='predictions',source=df_cdf,color='black',y_range_name='foo',size=9,legend='Prediction Trend')
        
    fig_list.line(over,pred,color='green',y_range_name='foo',legend='Prediction Trend')
    fig_list.circle(over,pred,color='black',y_range_name='foo',size=9,legend='Prediction Trend')
    fig_list.circle(over,[0.5]*len(over),y_range_name='foo',size=7,color='yellow')

    team_prob=Span(location=0.5,y_range_name='foo',dimension='width',line_color='pink',line_width=0.8)
        
    fig_list.renderers.extend([team_prob])
       
    fig_list.add_tools(HoverTool(tooltips=fig_hover))
        
    fig_list.legend.click_policy = 'hide'
	
    
    doc.add_root(fig_list)
    
def main():
   modify_doc(curdoc())

main()
