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
from bokeh.models.widgets import Tabs,Panel

# Hide some noisy warnings
logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)

def modify_doc(doc):
    year_list=[]
    fig_list=[]
    panel_list=[]
    tabs_list=[]
    for i in range(2008,2017):
        year_list.append(i)
        fig_list.append('fig_'+str(i))
        panel_list.append('panel_'+str(i))
    select_tools=['box_select', 'lasso_select', 'poly_select', 'tap', 'reset']

    csvdata0 = StringIO("""ind,Team1,is_batting_team,innings_over,innings_score,innings_wickets,score_target,total_runs,predictions
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

    csvdata1 = StringIO("""ind,Team1,is_batting_team,innings_over,innings_score,innings_wickets,score_target,total_runs,predictions,
    1,Deccan Chargers,1,1_1,2,1,-1,2,0.418462,
    2,Deccan Chargers,1,1_2,13,1,-1,11,0.383185,
    3,Deccan Chargers,1,1_3,15,1,-1,2,0.309114,
    4,Deccan Chargers,1,1_4,18,2,-1,3,0.519078,
    5,Deccan Chargers,1,1_5,23,2,-1,5,0.404831,
    6,Deccan Chargers,1,1_6,31,2,-1,8,0.41559,
    7,Deccan Chargers,1,1_7,45,2,-1,14,0.460154,
    8,Deccan Chargers,1,1_8,54,2,-1,9,0.597819,
    9,Deccan Chargers,1,1_9,59,3,-1,5,0.459813,
    10,Deccan Chargers,1,1_10,62,3,-1,3,0.378117,
    11,Deccan Chargers,1,1_11,65,3,-1,3,0.361208,
    12,Deccan Chargers,1,1_12,69,3,-1,4,0.341243,
    13,Deccan Chargers,1,1_13,74,3,-1,5,0.424273,
    14,Deccan Chargers,1,1_14,81,3,-1,7,0.474827,
    15,Deccan Chargers,1,1_15,101,3,-1,20,0.289117,
    16,Deccan Chargers,1,1_16,109,3,-1,8,0.301205,
    17,Deccan Chargers,1,1_17,115,5,-1,6,0.43711,
    18,Deccan Chargers,1,1_18,125,5,-1,10,0.485522,
    19,Deccan Chargers,1,1_19,134,5,-1,9,0.401706,
    20,Deccan Chargers,1,1_20,143,6,-1,9,0.555332,
    21,Deccan Chargers,0,2_1,1,0,143,1,0.257814,
    22,Deccan Chargers,0,2_2,5,0,143,4,0.23319,
    23,Deccan Chargers,0,2_3,16,0,143,11,0.164097,
    24,Deccan Chargers,0,2_4,21,1,143,5,0.156184,
    25,Deccan Chargers,0,2_5,33,1,143,12,0.106631,
    26,Deccan Chargers,0,2_6,36,1,143,3,0.088643,
    27,Deccan Chargers,0,2_7,42,2,143,6,0.120492,
    28,Deccan Chargers,0,2_8,53,2,143,11,0.128927,
    29,Deccan Chargers,0,2_9,59,3,143,6,0.102306,
    30,Deccan Chargers,0,2_10,69,3,143,10,0.11196,
    31,Deccan Chargers,0,2_11,78,3,143,9,0.087455,
    32,Deccan Chargers,0,2_12,79,4,143,1,0.064774,
    33,Deccan Chargers,0,2_13,91,4,143,12,0.080551,
    34,Deccan Chargers,0,2_14,99,4,143,8,0.089982,
    35,Deccan Chargers,0,2_15,103,6,143,4,0.112913,
    36,Deccan Chargers,0,2_16,108,7,143,5,0.133853,
    37,Deccan Chargers,0,2_17,113,8,143,5,0.429025,
    38,Deccan Chargers,0,2_18,117,8,143,4,0.932228,
    39,Deccan Chargers,0,2_19,129,9,143,12,0.923108,
    40,Deccan Chargers,0,2_20,137,9,143,8,1""")

    csvdata2 = StringIO("""ind,Team1,is_batting_team,innings_over,innings_score,innings_wickets,score_target,total_runs,predictions,
    0,Chennai Super Kings,1,1_1,4,0,-1,4,0.393378,
    1,Chennai Super Kings,1,1_2,6,0,-1,2,0.367356,
    2,Chennai Super Kings,1,1_3,13,0,-1,7,0.279421,
    3,Chennai Super Kings,1,1_4,20,0,-1,7,0.430166,
    4,Chennai Super Kings,1,1_5,29,0,-1,9,0.598353,
    5,Chennai Super Kings,1,1_6,40,0,-1,11,0.43039,
    6,Chennai Super Kings,1,1_7,43,0,-1,3,0.512654,
    7,Chennai Super Kings,1,1_8,44,1,-1,1,0.210863,
    8,Chennai Super Kings,1,1_9,49,2,-1,5,0.19324,
    9,Chennai Super Kings,1,1_10,58,2,-1,9,0.553489,
    10,Chennai Super Kings,1,1_11,67,2,-1,9,0.452511,
    11,Chennai Super Kings,1,1_12,68,3,-1,1,0.353449,
    12,Chennai Super Kings,1,1_13,80,3,-1,12,0.676368,
    13,Chennai Super Kings,1,1_14,91,3,-1,11,0.67737,
    14,Chennai Super Kings,1,1_15,108,3,-1,17,0.667306,
    15,Chennai Super Kings,1,1_16,127,3,-1,19,0.815298,
    16,Chennai Super Kings,1,1_17,139,3,-1,12,0.695107,
    17,Chennai Super Kings,1,1_18,146,4,-1,7,0.684177,
    18,Chennai Super Kings,1,1_19,157,4,-1,11,0.711988,
    19,Chennai Super Kings,1,1_20,168,5,-1,11,0.864396,
    20,Chennai Super Kings,0,2_1,0,0,168,0,0.979969,
    21,Chennai Super Kings,0,2_2,3,1,168,3,0.97662,
    22,Chennai Super Kings,0,2_3,9,1,168,6,0.979287,
    23,Chennai Super Kings,0,2_4,11,1,168,2,0.981812,
    24,Chennai Super Kings,0,2_5,21,1,168,10,0.97446,
    25,Chennai Super Kings,0,2_6,33,1,168,12,0.930217,
    26,Chennai Super Kings,0,2_7,38,1,168,5,0.953556,
    27,Chennai Super Kings,0,2_8,40,1,168,2,0.958383,
    28,Chennai Super Kings,0,2_9,43,1,168,3,0.982908,
    29,Chennai Super Kings,0,2_10,58,1,168,15,0.969361,
    30,Chennai Super Kings,0,2_11,67,1,168,9,0.965913,
    31,Chennai Super Kings,0,2_12,73,3,168,6,0.986988,
    32,Chennai Super Kings,0,2_13,80,3,168,7,0.990072,
    33,Chennai Super Kings,0,2_14,95,3,168,15,0.979524,
    34,Chennai Super Kings,0,2_15,101,5,168,6,0.991742,
    35,Chennai Super Kings,0,2_16,109,5,168,8,0.991574,
    36,Chennai Super Kings,0,2_17,114,6,168,5,0.992085,
    37,Chennai Super Kings,0,2_18,136,6,168,22,0.989687,
    38,Chennai Super Kings,0,2_19,142,8,168,6,0.990808,
    39,Chennai Super Kings,0,2_20,146,9,168,4,1""")

    csvdata3 = StringIO("""Ind,Team1,is_batting_team,innings_over,innings_score,innings_wickets,score_target,total_runs,predictions
    0,Chennai Super Kings,1,1_1,5,0,-1,5,0.502185
    1,Chennai Super Kings,1,1_2,16,0,-1,11,0.470899
    2,Chennai Super Kings,1,1_3,26,0,-1,10,0.529878
    3,Chennai Super Kings,1,1_4,36,0,-1,10,0.509338
    4,Chennai Super Kings,1,1_5,48,0,-1,12,0.725959
    5,Chennai Super Kings,1,1_6,56,0,-1,8,0.663792
    6,Chennai Super Kings,1,1_7,61,0,-1,5,0.535899
    7,Chennai Super Kings,1,1_8,73,0,-1,12,0.701697
    8,Chennai Super Kings,1,1_9,84,0,-1,11,0.702235
    9,Chennai Super Kings,1,1_10,94,0,-1,10,0.610184
    10,Chennai Super Kings,1,1_11,103,0,-1,9,0.669301
    11,Chennai Super Kings,1,1_12,121,0,-1,18,0.884473
    12,Chennai Super Kings,1,1_13,131,0,-1,10,0.892426
    13,Chennai Super Kings,1,1_14,143,0,-1,12,0.915736
    14,Chennai Super Kings,1,1_15,161,1,-1,18,0.902845
    15,Chennai Super Kings,1,1_16,167,1,-1,6,0.915348
    16,Chennai Super Kings,1,1_17,172,1,-1,5,0.92405
    17,Chennai Super Kings,1,1_18,188,1,-1,16,0.916971
    18,Chennai Super Kings,1,1_19,198,3,-1,10,0.882909
    19,Chennai Super Kings,1,1_20,205,5,-1,7,0.887388
    20,Chennai Super Kings,0,2_1,6,1,205,6,0.969379
    21,Chennai Super Kings,0,2_2,15,1,205,9,0.976162
    22,Chennai Super Kings,0,2_3,18,2,205,3,0.97587
    23,Chennai Super Kings,0,2_4,24,2,205,6,0.970926
    24,Chennai Super Kings,0,2_5,38,2,205,14,0.972437
    25,Chennai Super Kings,0,2_6,47,2,205,9,0.976438
    26,Chennai Super Kings,0,2_7,50,3,205,3,0.98391
    27,Chennai Super Kings,0,2_8,60,3,205,10,0.982048
    28,Chennai Super Kings,0,2_9,67,4,205,7,0.987823
    29,Chennai Super Kings,0,2_10,69,5,205,2,0.990036
    30,Chennai Super Kings,0,2_11,73,6,205,4,0.99111
    31,Chennai Super Kings,0,2_12,88,6,205,15,0.98725
    32,Chennai Super Kings,0,2_13,92,7,205,4,0.990497
    33,Chennai Super Kings,0,2_14,95,7,205,3,0.991381
    34,Chennai Super Kings,0,2_15,107,7,205,12,0.991421
    35,Chennai Super Kings,0,2_16,115,7,205,8,0.990994
    36,Chennai Super Kings,0,2_17,119,7,205,4,0.991025
    37,Chennai Super Kings,0,2_18,127,7,205,8,0.991513
    38,Chennai Super Kings,0,2_19,133,8,205,6,0.990154
    39,Chennai Super Kings,0,2_20,147,8,205,14,1""")

    csvdata4 = StringIO("""Ind,Team1,is_batting_team,innings_over,innings_score,innings_wickets,score_target,total_runs,predictions
    0,Chennai Super Kings,1,1_1,3,0,-1,3,0.415762
    1,Chennai Super Kings,1,1_2,6,0,-1,3,0.360532
    2,Chennai Super Kings,1,1_3,17,0,-1,11,0.359973
    3,Chennai Super Kings,1,1_4,31,0,-1,14,0.486336
    4,Chennai Super Kings,1,1_5,35,0,-1,4,0.435093
    5,Chennai Super Kings,1,1_6,54,0,-1,19,0.779399
    6,Chennai Super Kings,1,1_7,63,0,-1,9,0.574689
    7,Chennai Super Kings,1,1_8,69,0,-1,6,0.548259
    8,Chennai Super Kings,1,1_9,82,0,-1,13,0.604772
    9,Chennai Super Kings,1,1_10,86,0,-1,4,0.5344
    10,Chennai Super Kings,1,1_11,91,1,-1,5,0.708299
    11,Chennai Super Kings,1,1_12,104,1,-1,13,0.611238
    12,Chennai Super Kings,1,1_13,111,1,-1,7,0.721378
    13,Chennai Super Kings,1,1_14,128,1,-1,17,0.742085
    14,Chennai Super Kings,1,1_15,136,1,-1,8,0.716185
    15,Chennai Super Kings,1,1_16,146,1,-1,10,0.720047
    16,Chennai Super Kings,1,1_17,160,1,-1,14,0.606026
    17,Chennai Super Kings,1,1_18,171,2,-1,11,0.694927
    18,Chennai Super Kings,1,1_19,182,2,-1,11,0.788808
    19,Chennai Super Kings,1,1_20,190,3,-1,8,0.702081
    20,Chennai Super Kings,0,2_1,3,1,190,3,0.548742
    21,Chennai Super Kings,0,2_2,9,1,190,6,0.75047
    22,Chennai Super Kings,0,2_3,16,1,190,7,0.720721
    23,Chennai Super Kings,0,2_4,36,1,190,20,0.593561
    24,Chennai Super Kings,0,2_5,41,1,190,5,0.541887
    25,Chennai Super Kings,0,2_6,56,1,190,15,0.400409
    26,Chennai Super Kings,0,2_7,69,1,190,13,0.220827
    27,Chennai Super Kings,0,2_8,77,1,190,8,0.332827
    28,Chennai Super Kings,0,2_9,91,1,190,14,0.137678
    29,Chennai Super Kings,0,2_10,100,1,190,9,0.147544
    30,Chennai Super Kings,0,2_11,111,1,190,11,0.073038
    31,Chennai Super Kings,0,2_12,121,1,190,10,0.062771
    32,Chennai Super Kings,0,2_13,129,1,190,8,0.056692
    33,Chennai Super Kings,0,2_14,137,1,190,8,0.07344
    34,Chennai Super Kings,0,2_15,141,2,190,4,0.148054
    35,Chennai Super Kings,0,2_16,152,2,190,11,0.158153
    36,Chennai Super Kings,0,2_17,164,3,190,12,0.09867
    37,Chennai Super Kings,0,2_18,171,4,190,7,0.140318
    38,Chennai Super Kings,0,2_19,182,5,190,11,0.091502
    39,Chennai Super Kings,0,2_20,192,5,190,10,1""")

    csvdata5 = StringIO("""Ind,Team1,is_batting_team,innings_over,innings_score,innings_wickets,score_target,total_runs,predictions
    0,Mumbai Indians,1,1_1,8,1,-1,8,0.383851826
    1,Mumbai Indians,1,1_2,11,2,-1,3,0.323301822
    2,Mumbai Indians,1,1_3,16,2,-1,5,0.312742233
    3,Mumbai Indians,1,1_4,18,3,-1,2,0.380473137
    4,Mumbai Indians,1,1_5,25,3,-1,7,0.408334315
    5,Mumbai Indians,1,1_6,34,3,-1,9,0.395335644
    6,Mumbai Indians,1,1_7,40,3,-1,6,0.3998698
    7,Mumbai Indians,1,1_8,45,3,-1,5,0.307690442
    8,Mumbai Indians,1,1_9,50,3,-1,5,0.276083499
    9,Mumbai Indians,1,1_10,58,4,-1,8,0.328800946
    10,Mumbai Indians,1,1_11,65,4,-1,7,0.404826671
    11,Mumbai Indians,1,1_12,74,4,-1,9,0.25430271
    12,Mumbai Indians,1,1_13,84,4,-1,10,0.273796052
    13,Mumbai Indians,1,1_14,90,4,-1,6,0.306218386
    14,Mumbai Indians,1,1_15,100,4,-1,10,0.431241333
    15,Mumbai Indians,1,1_16,106,5,-1,6,0.456771851
    16,Mumbai Indians,1,1_17,112,5,-1,6,0.475304931
    17,Mumbai Indians,1,1_18,129,6,-1,17,0.554066896
    18,Mumbai Indians,1,1_19,135,7,-1,6,0.301482588
    19,Mumbai Indians,1,1_20,148,9,-1,13,0.469478905
    20,Mumbai Indians,0,2_1,2,2,148,2,0.620687664
    21,Mumbai Indians,0,2_2,5,3,148,3,0.654374719
    22,Mumbai Indians,0,2_3,12,3,148,7,0.562547326
    23,Mumbai Indians,0,2_4,22,3,148,10,0.735022187
    24,Mumbai Indians,0,2_5,29,3,148,7,0.787834764
    25,Mumbai Indians,0,2_6,35,4,148,6,0.855339348
    26,Mumbai Indians,0,2_7,38,5,148,3,0.889269471
    27,Mumbai Indians,0,2_8,41,6,148,3,0.923940063
    28,Mumbai Indians,0,2_9,50,6,148,9,0.916825712
    29,Mumbai Indians,0,2_10,54,6,148,4,0.913438201
    30,Mumbai Indians,0,2_11,57,7,148,3,0.954819858
    31,Mumbai Indians,0,2_12,59,8,148,2,0.964153171
    32,Mumbai Indians,0,2_13,67,8,148,8,0.964649677
    33,Mumbai Indians,0,2_14,73,8,148,6,0.972607315
    34,Mumbai Indians,0,2_15,83,8,148,10,0.971883237
    35,Mumbai Indians,0,2_16,93,8,148,10,0.973150194
    36,Mumbai Indians,0,2_17,97,8,148,4,0.976215482
    37,Mumbai Indians,0,2_18,99,9,148,2,0.978779495
    38,Mumbai Indians,0,2_19,107,9,148,8,0.970914602
    39,Mumbai Indians,0,2_20,125,9,148,18,1""")

    csvdata6 = StringIO("""Ind,Team1,is_batting_team,innings_over,innings_score,innings_wickets,score_target,total_runs,predictions
    0,Kings XI Punjab,1,1_1,9,0,-1,9,0.543645501
    1,Kings XI Punjab,1,1_2,15,0,-1,6,0.528323352
    2,Kings XI Punjab,1,1_3,21,0,-1,6,0.559491277
    3,Kings XI Punjab,1,1_4,24,1,-1,3,0.293968648
    4,Kings XI Punjab,1,1_5,30,1,-1,6,0.293804467
    5,Kings XI Punjab,1,1_6,32,2,-1,2,0.078102246
    6,Kings XI Punjab,1,1_7,36,2,-1,4,0.081196286
    7,Kings XI Punjab,1,1_8,50,2,-1,14,0.112934083
    8,Kings XI Punjab,1,1_9,54,2,-1,4,0.114527762
    9,Kings XI Punjab,1,1_10,58,2,-1,4,0.102472603
    10,Kings XI Punjab,1,1_11,67,2,-1,9,0.148384064
    11,Kings XI Punjab,1,1_12,82,2,-1,15,0.274380416
    12,Kings XI Punjab,1,1_13,92,2,-1,10,0.365836263
    13,Kings XI Punjab,1,1_14,111,2,-1,19,0.57075727
    14,Kings XI Punjab,1,1_15,131,2,-1,20,0.513468504
    15,Kings XI Punjab,1,1_16,140,2,-1,9,0.519275069
    16,Kings XI Punjab,1,1_17,159,2,-1,19,0.656871736
    17,Kings XI Punjab,1,1_18,170,4,-1,11,0.720629454
    18,Kings XI Punjab,1,1_19,187,4,-1,17,0.682885289
    19,Kings XI Punjab,1,1_20,199,4,-1,12,0.687032461
    20,Kings XI Punjab,0,2_1,10,1,199,10,0.597744465
    21,Kings XI Punjab,0,2_2,19,1,199,9,0.789518118
    22,Kings XI Punjab,0,2_3,31,1,199,12,0.409407139
    23,Kings XI Punjab,0,2_4,40,1,199,9,0.479550809
    24,Kings XI Punjab,0,2_5,48,1,199,8,0.680699885
    25,Kings XI Punjab,0,2_6,59,1,199,11,0.508752644
    26,Kings XI Punjab,0,2_7,67,2,199,8,0.782000065
    27,Kings XI Punjab,0,2_8,73,2,199,6,0.74414736
    28,Kings XI Punjab,0,2_9,87,2,199,14,0.642163515
    29,Kings XI Punjab,0,2_10,89,2,199,2,0.697236121
    30,Kings XI Punjab,0,2_11,107,2,199,18,0.565130949
    31,Kings XI Punjab,0,2_12,110,2,199,3,0.628820539
    32,Kings XI Punjab,0,2_13,128,2,199,18,0.450481653
    33,Kings XI Punjab,0,2_14,142,3,199,14,0.27497229
    34,Kings XI Punjab,0,2_15,151,3,199,9,0.274347305
    35,Kings XI Punjab,0,2_16,161,4,199,10,0.300096929
    36,Kings XI Punjab,0,2_17,179,6,199,18,0.122425318
    37,Kings XI Punjab,0,2_18,185,6,199,6,0.133222431
    38,Kings XI Punjab,0,2_19,195,7,199,10,0.069089293
    39,Kings XI Punjab,0,2_20,200,7,199,5,1""")

    csvdata7 = StringIO("""Ind,Team1,is_batting_team,innings_over,innings_score,innings_wickets,score_target,total_runs,predictions
    0,Mumbai Indians,1,1_1,1,1,-1.0,1,0.33816811442375183
    1,Mumbai Indians,1,1_2,17,1,-1.0,16,0.6274080872535706
    2,Mumbai Indians,1,1_3,28,1,-1.0,11,0.693503201007843
    3,Mumbai Indians,1,1_4,40,1,-1.0,12,0.7188851833343506
    4,Mumbai Indians,1,1_5,47,1,-1.0,7,0.9215619564056396
    5,Mumbai Indians,1,1_6,61,1,-1.0,14,0.8250930309295654
    6,Mumbai Indians,1,1_7,69,1,-1.0,8,0.9360390901565552
    7,Mumbai Indians,1,1_8,78,1,-1.0,9,0.9412041306495667
    8,Mumbai Indians,1,1_9,88,1,-1.0,10,0.9511234164237976
    9,Mumbai Indians,1,1_10,98,1,-1.0,10,0.9544880390167236
    10,Mumbai Indians,1,1_11,110,1,-1.0,12,0.9345460534095764
    11,Mumbai Indians,1,1_12,120,2,-1.0,10,0.9496986269950867
    12,Mumbai Indians,1,1_13,125,3,-1.0,5,0.9400908946990967
    13,Mumbai Indians,1,1_14,134,3,-1.0,9,0.9318138957023621
    14,Mumbai Indians,1,1_15,146,3,-1.0,12,0.9177364110946655
    15,Mumbai Indians,1,1_16,150,3,-1.0,4,0.9325587153434753
    16,Mumbai Indians,1,1_17,173,3,-1.0,23,0.923777163028717
    17,Mumbai Indians,1,1_18,183,3,-1.0,10,0.9533054232597351
    18,Mumbai Indians,1,1_19,191,4,-1.0,8,0.94910728931427
    19,Mumbai Indians,1,1_20,202,5,-1.0,11,0.9119037389755249
    20,Mumbai Indians,0,2_1,5,0,202.0,5,0.9706622958183289
    21,Mumbai Indians,0,2_2,12,0,202.0,7,0.9620175361633301
    22,Mumbai Indians,0,2_3,15,0,202.0,3,0.9835399389266968
    23,Mumbai Indians,0,2_4,21,0,202.0,6,0.9753340482711792
    24,Mumbai Indians,0,2_5,26,1,202.0,5,0.9780483245849609
    25,Mumbai Indians,0,2_6,31,1,202.0,5,0.9784472584724426
    26,Mumbai Indians,0,2_7,38,1,202.0,7,0.979611337184906
    27,Mumbai Indians,0,2_8,50,1,202.0,12,0.9792531728744507
    28,Mumbai Indians,0,2_9,57,1,202.0,7,0.9798712134361267
    29,Mumbai Indians,0,2_10,67,1,202.0,10,0.9807290434837341
    30,Mumbai Indians,0,2_11,81,1,202.0,14,0.9787614345550537
    31,Mumbai Indians,0,2_12,89,2,202.0,8,0.9842265248298645
    32,Mumbai Indians,0,2_13,98,2,202.0,9,0.9859371781349182
    33,Mumbai Indians,0,2_14,102,3,202.0,4,0.987149715423584
    34,Mumbai Indians,0,2_15,112,4,202.0,10,0.988625168800354
    35,Mumbai Indians,0,2_16,125,5,202.0,13,0.9873172640800476
    36,Mumbai Indians,0,2_17,132,6,202.0,7,0.9892262816429138
    37,Mumbai Indians,0,2_18,137,7,202.0,5,0.9905507564544678
    38,Mumbai Indians,0,2_19,140,8,202.0,3,0.9895074963569641
    39,Mumbai Indians,0,2_20,161,8,202.0,21,1.0""")

    csvdata8 = StringIO(""",Team1,is_batting_team,innings_over,innings_score,innings_wickets,score_target,total_runs,predictions
    0,Sunrisers Hyderabad,1,1_1,7,0,-1.0,7,0.2511650025844574
    1,Sunrisers Hyderabad,1,1_2,12,0,-1.0,5,0.40610888600349426
    2,Sunrisers Hyderabad,1,1_3,21,0,-1.0,9,0.439710408449173
    3,Sunrisers Hyderabad,1,1_4,27,0,-1.0,6,0.4730672240257263
    4,Sunrisers Hyderabad,1,1_5,46,0,-1.0,19,0.400312602519989
    5,Sunrisers Hyderabad,1,1_6,59,0,-1.0,13,0.4444854259490967
    6,Sunrisers Hyderabad,1,1_7,65,1,-1.0,6,0.24245789647102356
    7,Sunrisers Hyderabad,1,1_8,75,1,-1.0,10,0.17398516833782196
    8,Sunrisers Hyderabad,1,1_9,88,1,-1.0,13,0.24258705973625183
    9,Sunrisers Hyderabad,1,1_10,97,2,-1.0,9,0.14986717700958252
    10,Sunrisers Hyderabad,1,1_11,103,2,-1.0,6,0.15866513550281525
    11,Sunrisers Hyderabad,1,1_12,116,2,-1.0,13,0.4142865240573883
    12,Sunrisers Hyderabad,1,1_13,120,2,-1.0,4,0.2560994327068329
    13,Sunrisers Hyderabad,1,1_14,127,3,-1.0,7,0.2799372673034668
    14,Sunrisers Hyderabad,1,1_15,140,3,-1.0,13,0.55829918384552
    15,Sunrisers Hyderabad,1,1_16,147,4,-1.0,7,0.3921412229537964
    16,Sunrisers Hyderabad,1,1_17,156,5,-1.0,9,0.3356223404407501
    17,Sunrisers Hyderabad,1,1_18,168,6,-1.0,12,0.3988121747970581
    18,Sunrisers Hyderabad,1,1_19,184,7,-1.0,16,0.6285400986671448
    19,Sunrisers Hyderabad,1,1_20,208,7,-1.0,24,0.6917642951011658
    20,Sunrisers Hyderabad,0,2_1,5,0,208.0,5,0.8255436420440674
    21,Sunrisers Hyderabad,0,2_2,18,0,208.0,13,0.8321638107299805
    22,Sunrisers Hyderabad,0,2_3,26,0,208.0,8,0.8851979970932007
    23,Sunrisers Hyderabad,0,2_4,42,0,208.0,16,0.8368229866027832
    24,Sunrisers Hyderabad,0,2_5,55,0,208.0,13,0.39258313179016113
    25,Sunrisers Hyderabad,0,2_6,59,0,208.0,4,0.8662683367729187
    26,Sunrisers Hyderabad,0,2_7,69,0,208.0,10,0.8306481838226318
    27,Sunrisers Hyderabad,0,2_8,79,0,208.0,10,0.8281657695770264
    28,Sunrisers Hyderabad,0,2_9,100,0,208.0,21,0.26929566264152527
    29,Sunrisers Hyderabad,0,2_10,112,0,208.0,12,0.10838765650987625
    30,Sunrisers Hyderabad,0,2_11,120,1,208.0,8,0.18792183697223663
    31,Sunrisers Hyderabad,0,2_12,129,1,208.0,9,0.1692996770143509
    32,Sunrisers Hyderabad,0,2_13,141,2,208.0,12,0.10891570150852203
    33,Sunrisers Hyderabad,0,2_14,149,3,208.0,8,0.13900497555732727
    34,Sunrisers Hyderabad,0,2_15,158,3,208.0,9,0.3233165144920349
    35,Sunrisers Hyderabad,0,2_16,162,4,208.0,4,0.8817701935768127
    36,Sunrisers Hyderabad,0,2_17,172,5,208.0,10,0.9066932201385498
    37,Sunrisers Hyderabad,0,2_18,179,5,208.0,7,0.9411659240722656
    38,Sunrisers Hyderabad,0,2_19,191,6,208.0,12,0.9563006162643433
    39,Sunrisers Hyderabad,0,2_20,200,7,208.0,9,1.0""")

    df1 = pd.read_csv(csvdata0, sep=",")
    df2 = pd.read_csv(csvdata1, sep=",")
    df3 = pd.read_csv(csvdata2, sep=",")
    df4 = pd.read_csv(csvdata3, sep=",")
    df5 = pd.read_csv(csvdata4, sep=",")
    df6 = pd.read_csv(csvdata5, sep=",")
    df7 = pd.read_csv(csvdata6, sep=",")
    df8 = pd.read_csv(csvdata7, sep=",")
    df9 = pd.read_csv(csvdata8, sep=",")

    csvdata=[df1,df2,df3,df4,df5,df6,df7,df8,df9]

    for i in range(0,9):
        df=csvdata[i]
        over=list(df.innings_over)
        score=list(df.innings_score)
        pred=list(df.predictions)
        color_innings=['blue']*20 + ['red']*20
        
        
        #
        #formatting colors for innings/batting
        df['color_innings']=df.apply(lambda x:'Blue' if x['is_batting_team']==1 else 'Red',axis=1)
        #
        
        select_tools=['box_select', 'lasso_select', 'poly_select', 'tap', 'reset','hover','wheel_zoom']
        #total runs
        
        df_cdf=ColumnDataSource(df)
        #view_aus=CDSView(source=vCDF,filters=[GroupFilter(column_name='LOCATION',group='AUS')])
        view_cdf_1=CDSView(source=df_cdf,filters=[GroupFilter(column_name='is_batting_team',group='1')])
        view_cdf_2=CDSView(source=df_cdf,filters=[GroupFilter(column_name='is_batting_team',group='0')])
        
        
        fig_list[i]=figure(x_range=over,plot_height=500,plot_width=1000,tools=select_tools,tooltips=[('Team','@Team1'),('Innings Score','@innings_score')])
        
        fig_list[i].extra_y_ranges={"foo":Range1d(start=0,end=1)}
        fig_list[i].add_layout(LinearAxis(y_range_name='foo'),'right')
        fig_list[i].y_range.start=0
        #fig_list[i].legend.click_policy = 'hide'
        
        fig_list[i].vbar(x='innings_over',top='total_runs',source=df_cdf,width=0.9,color='color_innings',legend='Score')
        
        #
        fig_list[i].line(x='innings_over',y='predictions',source=df_cdf,color='green',y_range_name='foo',legend='Prediction Trend')
        fig_list[i].circle(x='innings_over',y='predictions',source=df_cdf,color='black',y_range_name='foo',size=9,legend='Prediction Trend')
        #
        
        #fig_list[i].line(over,pred,color='green',y_range_name='foo',legend='Prediction Trend')
        #fig_list[i].circle(over,pred,color='black',y_range_name='foo',size=9,legend='Prediction Trend')
        #fig_list[i].circle(over,[0.5]*len(over),y_range_name='foo',size=7,color='yellow')

        team_prob=Span(location=0.5,y_range_name='foo',dimension='width',line_color='pink',line_width=0.8)
        
        fig_list[i].renderers.extend([team_prob])
       
        # fig_list[i].add_tools(HoverTool(tooltips=fig_hover))
        
        fig_list[i].legend.click_policy = 'hide'
        panel_list[i]=Panel(child=fig_list[i],title=str(year_list[i]))
        tabs_list.append(panel_list[i])
    
    fig_tab=Tabs(tabs=tabs_list)    
    doc.add_root(fig_tab)
    
def main():
    modify_doc(curdoc())

main()