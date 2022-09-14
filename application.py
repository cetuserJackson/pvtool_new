import os
import pathlib
import re
# from turtle import color
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import numpy as np
from dash import dash_table
from sklearn import linear_model
# import cufflinks as cf

# Initialize app

dash_app = dash.Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)
dash_app.title = "Pressure Vessel Tool"
app = dash_app.server

# Load data


dtcols = ['Parameter', 'Imperial', 'Units', 'Metric', 'Unit']

YEARS = [2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015]

tube_lengths = [30, 40, 50, 60, 70, 80]

tube_OD = [2,  20,  40,  60,  80]

tube_plies = [40, 120, 280, 440, 600]

wall_thicknesses = [5, 50, 100, 150, 200, 250]

BINS = [
    "0-2",
    "2.1-4",
    "4.1-6",
    "6.1-8",
    "8.1-10",
    "10.1-12",
    "12.1-14",
    "14.1-16",
    "16.1-18",
    "18.1-20",
    "20.1-22",
    "22.1-24",
    "24.1-26",
    "26.1-28",
    "28.1-30",
    ">30",
]

DEFAULT_COLORSCALE = [
    "#f2fffb",
    "#bbffeb",
    "#98ffe0",
    "#79ffd6",
    "#6df0c8",
    "#69e7c0",
    "#59dab2",
    "#45d0a5",
    "#31c194",
    "#2bb489",
    "#25a27b",
    "#1e906d",
    "#188463",
    "#157658",
    "#11684d",
    "#10523e",
]

DEFAULT_OPACITY = 0.8


## Create Depths and Pressures for Contour Plot

trace_depths =  go.Contour(
                            # name = 'Center of Gravity',
                            z=[[120, 120, 120, 120, 120],
                            [110, 110, 110, 110, 110],
                            [100, 100, 100, 100, 100],
                            [90, 90, 90, 90, 90],
                            [80, 80, 80, 80, 80],
                            [70, 70, 70, 70, 70],
                            [60, 60, 60, 60, 60],
                            [50, 50, 50, 50, 50],
                            [40, 40, 40, 40, 40],
                            [20, 20, 20, 20, 20],
                            [0, 0, 0, 0, 0]
                            ],
                            x=[0, 2, 4 , 6, 8], # horizontal axis
                            y=[-12000,-11000,-10000, -9000, -8000, -7000, -6000, -5000, -4000, -2000,  0], # vertical axis
                            colorbar=dict(
                                title='Pressure Contours (MPa)', # title here
                                titleside='right',
                                titlefont=dict(
                                    size=14,
                                    # family='Arial, sans-serif',
                                    color = '#2cfec1'),
                                # nticks=10, 
                                ticks='outside',
                                ticklen=5, 
                                tickwidth=1,
                                showticklabels=True,
                                tickangle=0, 
                                tickfont_size=12,
                                tickcolor = '#2cfec1',
                                tickfont = dict(
                                    color = '#2cfec1')
                            ),
                            colorscale = 'Darkmint'
                        )


## Make models
# datain = pd.read_csv(r'C:\Users\JacksonKoelher\try\OTA\underpressure\pressure_vessel_data\underpressuredata1.csv')
datain =  pd.read_csv('assets/data/underpressuredata1.csv')

X = datain[['OD', 'Length', 'Shell Failure']]
y = datain['Wall Thickness']

wallthick_model = linear_model.LinearRegression()
wallthick_model.fit(X, y)

buckleX = datain[['OD', 'Length', 'Buckling Failure']]
buckley = datain['Wall Thickness']

buckling_model = linear_model.LinearRegression()
buckling_model.fit(buckleX, buckley)

# App layout

dash_app.layout = dbc.Container(
#     id="root",
#     children=[
        # html.Div(
        #     id="header",
        #     children=[
        #         # html.A(
        #         #     html.Img(id="logo", src=dash_app.get_asset_url("CET-LOGO.png")),
        #         #     href="https://www.compositeenergytechnologies.com/",
        #         # ),
        #         html.H3( children="Underwater Carbon Fiber Pressure Vessel Design Tool"),
        #         # html.P(
        #         #     id="description",
        #         #     children="Since 2019, CET has been working with the Office of Naval Research (ONR) to develop and validate carbon fiber \
        #         #         solutions for Full Ocean Depth (6,000 m) underwater pressure vessels.  Through comprehensive engineering studies \
        #         #         conducted in partnership with the College of Engineering at University of Rhode Island, CET has developed engineering \
        #         #         models to optimize the fabrication of underwater carbon fiber pressure vessels.  These models have been thoroughly \
        #         #         validated and proven through testing at the Woods Hole Oceanographic Institute (WHOI) Hydrostatic Test Facility.  \
        #         #         Please contact STAYDRY@USACET.COM for more information.",
        #         # ),
        #         html.Div(   id="description",
        #                     children = [
        #                         html.H6(children="User Defined Parameter", style = { 'width' : '40%', 'display': 'inline-block' }), html.H6(children="Driven Value", style = {'display': 'inline-block','color': '#2cfec1'}),
        #                     ])

        #     ],
        # ),
        # html.Div(
            # id="app-container",
            children=[




                html.Div(
                    id="left-column",
                    children=[

                                html.H3(children="Underwater Carbon Fiber Pressure Vessel Design Tool", className = "container-title", style={'textAlign': 'center'}),

                                html.Br(),

                                html.Div(
                                    className="control-row-1",
                                    children=[
                                                html.Div(
                                                    className="values-area",
                                                    children=[

                                                                # html.Div(
                                                                #     className="control-row-1",
                                                                #     children=[
                                                                #         # html.H3("Tube Outer Diameter (in):"),
                                                                #         # html.H5( 'Enter Email to Use Tool', className="dim-title"),
                                                                #         # html.H5( id="tube-od-output", className="dim-value"),
                                                                #         dcc.Input(id="email-enter", type="email", placeholder="Enter Email to Use Tool", 
                                                                #                             className="dim-email"),
                                                                #         html.Div(id = 'div-button', children = [
                                                                #                                                 html.Button('Submit',
                                                                                                                
                                                                #                                                 id='button-submit',
                                                                #                                                 n_clicks=0,
                                                                #                                                 style = { 'color': '#2cfec1'})
                                                                #                                             ]), #end div
                                                                #         # html.H5("Button", className="dim-unit"),
                                                                #     ]
                                                                # ),

                                                                html.Div(   id="description",
                                                                            children = [
                                                                                html.H6(children="User Defined Parameter", style = { 'width' : '60%', 'display': 'inline-block' }),
                                                                                html.H6(children="Driven Value", style = {'display': 'inline-block','color': '#2cfec1'}),
                                                                            ]),

                                                                html.H3('Inputs', className="container-label"),

                                                                html.Div(
                                                                    className="control-row-1",
                                                                    children=[
                                                                        
                                                                        html.H5('Solve for:', className="unit-title", style={'margin-right': '2em'}),
                                                                        
                                                                        dcc.RadioItems( id = 'solve', 
                                                                                            options=[
                                                                                                        {'label': 'Outer Diameter', 'value': 1},
                                                                                                        {'label': 'Inner Diameter', 'value': 2},
                                                                                                    ],
                                                                                                    value=2,
                                                                                            style=dict(
                                                                                                    width='70%',
                                                                                                    verticalAlign="middle"
                                                                                                ),
                                                                                            className="unit-option"
                                                                                        ),
                                                                    ]
                                                                ),

                                                                html.Br(),

                                                                html.Div(
                                                                    className="control-row-1",
                                                                    children=[
                                                                        # html.H3("Tube Outer Diameter (in):"),
                                                                        html.H5( id = "id_od_text", className="dim-title"),
                                                                        # html.H5( id="tube-od-output", className="dim-value"),
                                                                        dcc.Input(id="tube-od", type="number", value = 21, debounce=True, 
                                                                                            className="dim-value", min = 1, max = 40),
                                                                        html.H5("(in)", className="dim-unit"),
                                                                    ]
                                                                ),


                                                                html.Div(
                                                                    className="control-row-1",
                                                                    children=[
                                                                        html.H5("Tube Length:", className="dim-title"),
                                                                        dcc.Input(id="tube-length", type="number", value = 50, debounce=True, 
                                                                                            className="dim-value", min = 2, max = 100),
                                                                        # html.H5( id="tube-length-output", className="dim-value"),
                                                                        html.H5("(in)", className="dim-unit"),
                                                                    ]
                                                                ),


                                                                html.Div(
                                                                    className="control-row-1",
                                                                    children=[

                                                                        html.H5("Rated Depth:", className="dim-title"),
                                                                        
                                                                        dcc.Input(id="input-depth", type="number", placeholder="depth", value = 6000, debounce=True,
                                                                                            className="dim-value", min = 0, max = 20000),

                                                                        html.H5("(m)", className="dim-unit"),

                                                                        html.Div(html.H5(id="input-pressure"), hidden = True)
                                                                    ]
                                                                ),


                                                                html.Div(
                                                                    className="control-row-1",
                                                                    children=[
                                                                        html.H5("Safety Factor:", className="dim-title"),
                                                                        # html.Div(dcc.Input(id="input-sf", type="number", value = 1.5, debounce=True, ),
                                                                        #                     style = { 'width' : '10%', 'display': 'inline-block' }),
                                                                        dcc.Input(id="input-sf", type="number", value = 1.5, debounce=True, 
                                                                                            className="dim-value", min = 0.5, max = 10),

                                                                        html.H5("   ", className="dim-unit"),
                                                                    ]
                                                                ),

                                                                html.Br(),

                                                                html.H3('Calculated Values', className="container-label"),
                                                                html.Br(),

                                                                html.Div(
                                                                    className="control-row-1",
                                                                    children=[
                                                                        # html.H5("Inner Diameter (in):"),
                                                                        html.H5(id="id_od_output", className="dim-title"),
                                                                        html.H5(className="bright-value", id="inner-diameter-output"),
                                                                        html.H5("(in)", className="dim-unit"),
                                                                    ]
                                                                ),
                                                                # html.Br(),

                                                                html.Div(
                                                                    className="control-row-1",
                                                                    children=[
                                                                        html.H5("Weight:", className="dim-title"),
                                                                        html.H5(className="bright-value", id="weight-output"),
                                                                        html.H5("(lbs)", className="dim-unit"),
                                                                        
                                                                    ]
                                                                ),
                                                                # html.Br(),

                                                                # html.Br(),
                                                                html.Div(
                                                                    # className="control-row-1",
                                                                    children=[
                                                                        html.H5("Wall Thickness:", className="dim-title"),
                                                                        html.H5(className="bright-value", id="thickness-wall-output"),
                                                                        html.H5("(in)", className="dim-unit"),
                                                                    ],
                                                                    hidden=True
                                                                ), 
                                                                # html.Br(),
                                                                html.Div(
                                                                    className="control-row-1",
                                                                    children=[
                                                                        html.H5("Maximum Depth:", className="dim-title"),
                                                                        html.H5( id='failure_depth', className="bright-value"),
                                                                        html.H5("(m)", className="dim-unit"),
                                                                    ]
                                                                ),


                                                                html.Div(
                                                                    # className="control-row-1",
                                                                    children=[
                                                                        html.H5("Implosion Pressure:", className="dim-title"),
                                                                        html.H5(className="bright-value", id='implosion-pressure-output'),
                                                                        html.H5("(MPa)", className="dim-unit"),
                                                                    ],
                                                                    hidden=True
                                                                ),

                                                                html.Div(
                                                                    # className="control-row-1",
                                                                    children=[
                                                                        html.H5("Number of Plies :"),
                                                                        html.H5(className="bright-value", id="tube-plies-output"),
                                                                    ],
                                                                    hidden=True
                                                                ), 
                                                                

                                                                html.Div(
                                                                    # className="control-row-1",
                                                                    children=[
                                                                        html.H5("Wall Thickness (mm):"),
                                                                        html.H5(className="bright-value", id="wall-thickness-output"),
                                                                    ],
                                                                    hidden=True
                                                                ),


                                                                html.Div(
                                                                    # className="control-row-1",
                                                                    children=[
                                                                        html.H5("Length / OD:"),
                                                                        html.H5(className="bright-value", id="length-diameter-output"),
                                                                    ],
                                                                    hidden=True
                                                                ),
                                                                # html.Br(),

                                                                html.Div(
                                                                    # className="control-row-1",
                                                                    children=[
                                                                        html.H5("Thickness / OD:"),
                                                                        html.H5(className="bright-value", id="thickness-diameter-output"),
                                                                    ],
                                                                    hidden=True
                                                                ),
                                                                # html.Br(),

                                                                html.Div(
                                                                    # className="control-row-1",
                                                                    children=[
                                                                        html.H5("Ply Thickness (mm):"),
                                                                        # html.H5(className="bright-value", id="input-thickness", 0.45),
                                                                        html.H5("0.45"),
                                                                    ],
                                                                    hidden=True
                                                                ),

                                                                


                                                                html.Div(html.H5(className="bright-value", id="volume-output"), hidden = True)

                                                            ],
                                                        ),
                                        html.Div(
                                                        className="sliders-area",
                                                        children=[
                                                                    # html.Br(),
                                                                    dcc.Graph( id = 'vessel-plot', style={'height': '70vh'}),       

                                                                ],
                                                            ),

                                    ]
                                ),


                    ],
                ),

            ],
            # className="all",
            style={"height": "100vh"},
            fluid=True,
            # fluid=True
        )
#     ],
# )



## Change text between outer and inner diameter
@dash_app.callback(
    [Output("id_od_text", "children"),
    Output("id_od_output", "children")],
    Input("solve", "value"),
)
def update_output1(input1):
    if input1 == 1:
        return "Tube Inner Diameter:", "Outer Diameter:"
    if input1 == 2:
        return "Tube Outer Diameter:", "Inner Diameter:"

@dash_app.callback(
    Output("thickness-wall-output", "children"),
    #  Output("failure_type", "children")],
    Input("tube-od", "value"),
    Input("failure_depth", "children"), 
    Input("tube-length", "value")
     ,
)
def update_output2(tubeod, depthin, lengthin):

    # wall_thick = round((tubeod * 1/10 * implosion_pressure / 90), 2)
    # wall_thick = tubeod
    wall_thickshell = wallthick_model.predict([[tubeod, lengthin, depthin]])[0]

    wall_thickbuck = buckling_model.predict([[tubeod, lengthin, depthin]])[0]

    if wall_thickshell > wall_thickbuck:
        wall_thick = wall_thickshell
        failmode = 'Shell'
    else:
        wall_thick = wall_thickbuck
        failmode = 'Buckling'

    return wall_thick


@dash_app.callback(
    [
    
    Output("input-pressure", "children")],

    Input("input-depth", "value"),
)
def update_output4(depth):
    
    pressure_depth = round(( depth / 1000 ) * 10.1531, 2)

    return [pressure_depth]

@dash_app.callback(
    [
    
    Output("failure_depth", "children")],

    [
    Input("input-depth", "value"),
    Input("input-sf", "value"),]
)
def update_output6(depth, safety_factor):
    
    fail_depth = round(depth * safety_factor, 2)

    return [fail_depth]



##Calculate Implosion
@dash_app.callback(
    [
     Output("implosion-pressure-output", "children"),
    #  Output("failure-type-output", "children"),
    ],
    [

    Input("input-pressure", "children"),
    Input("input-sf", "value"),
    
    ]

)
def update_outputimp(pressure, safety_factor):

    safety_factor_out = safety_factor

    implosion_pressure = round( pressure * safety_factor_out, 3)

    #calculated failure is via buckling, transition, or strength.
    fail_type = 'Buckling'

    return [implosion_pressure]




##Calculate Variables of Interest
@dash_app.callback(
    [Output("inner-diameter-output", "children"),
     Output("wall-thickness-output", "children"),
    #  Output("implosion-pressure-output", "children"),
    #  Output("SF-output", "children"),
     Output("length-diameter-output", "children"),
     Output("thickness-diameter-output", "children"),
    #  Output("safety-factor-output", "children"),
     Output("weight-output", "children"),
     Output("volume-output", "children"),
     Output("tube-plies-output", "children")
    ],
    [
    Input("tube-length", "value"),
    Input("tube-od", "value"),
    Input("thickness-wall-output", "children"),
    # Input("input-thickness", "value"),
    Input("input-pressure", "children"),
    Input("input-sf", "value"),
    Input("solve", "value")
    
    ]

)
def update_output5(length, od, wallthick1, pressure, safety_factor, input1):

    plythickness = 0.45 

    wallthick = wallthick1

    plies = round( wallthick / plythickness , 0)

    wall_thickness = plies * plythickness 

    wall_thicknessin = round( wall_thickness / 25.4 , 2)

    inner_diameter = round( od - 2 * ( wall_thickness / 25.4 ), 3)

    if input1 == 1:
        calc_od_id = round( od + 2 * ( wall_thickness / 25.4 ), 3)
        odreal = round( od + 2 * ( wall_thickness / 25.4 ), 3)
        idreal = od
    if input1 == 2:
        calc_od_id = inner_diameter
        odreal = od
        idreal = inner_diameter


    length_od = round( length / odreal, 3)

    thick_od = round( wall_thicknessin / odreal, 3)

    # wall_thickness_factor = (plies/500)**(1/5)

    # safety_factor_in = -0.0006*length_od**4 + 0.017*length_od**3 - 0.1645*length_od**2 + 0.4492*length_od + 1.4138

    # safety_factor_out = round( safety_factor_in * wall_thickness_factor, 3)

    sf = 1.678

    # safety_factor_out = safety_factor

    # implosion_pressure = round( pressure * safety_factor_out, 3)

    ## Calculate Volume and Weight
    volume = round(( np.pi*( odreal / 2 )**2 - np.pi*( idreal / 2 )**2 ) * length, 2)
    weight = round(volume * 1.63871e-5 * 1625 * 2.2, 2)

    return calc_od_id, wall_thickness, length_od, thick_od, weight, volume, plies


@dash_app.callback(
    [Output("vessel-plot", "figure"),
    ],
    [
    Input("tube-length", "value"),
    Input("tube-od", "value"),
    Input("tube-plies-output", "children"),
    # Input("input-thickness", "value"),
    Input("input-pressure", "children"),
    Input("solve", "value")
    ]

)
def create_vessel(length, od, plies, pressure, input1):

    thickness = 0.45

    wall_thickness = round( (plies * thickness)/25.4, 3)

    if input1 == 1:
        calc_od_id = round( od + 2 * ( wall_thickness ), 3)
        odreal = round( od + 2 * ( wall_thickness  ), 3)
        idreal = od
    if input1 == 2:
        calc_od_id = round( od - 2 * ( wall_thickness ), 3)
        odreal = od
        idreal = calc_od_id

    Outer_Diameter = odreal

    Inner_Diameter = idreal

    X, Y, Z = np.mgrid[0:length:40j, -Outer_Diameter:Outer_Diameter:40j, -Outer_Diameter:Outer_Diameter:20j]

    ##Safety Figure Calcs
    length_od = round( length / Outer_Diameter, 3)

    plot_ratio = round( length / (Outer_Diameter * 2), 1)

    wall_thickness_factor = (plies/500)**(1/5)

    safety_factor_in = -0.0006*length_od**4 + 0.017*length_od**3 - 0.1645*length_od**2 + 0.4492*length_od + 1.4138

    safety_factor_out = safety_factor_in * wall_thickness_factor

    # ##Create trace over other values
    # od_lengths = np.linspace(0.5, 10, 40)
    # l_safety_factors = wall_thickness_factor*(-0.0006*od_lengths**4 + 0.017*od_lengths**3 - 0.1645*od_lengths**2 + 0.4492*od_lengths + 1.4138) 
    # l_implosion_pressure =  -1 * pressure * l_safety_factors
    # ##
    # d = {'length': [length],
    #      'OD': [Outer_Diameter],
    #      'ID': [ Inner_Diameter],
    #      'Thickness': [ wall_thickness]}

    # dft = pd.DataFrame(d)

    # dftt = pd.concat([dft] * len(X.flatten()), ignore_index=True)

    # new_customdatadf  = np.stack((dftt['length'], dftt['OD'], dftt['ID'], dftt['Thickness']))

    maxd = (Outer_Diameter/2)**2

    mind = (Inner_Diameter / 2)**2

    values = X * X * 0 + Y * Y + Z * Z

    figz = go.Figure(data=go.Isosurface(
        x=X.flatten(),
        y=Y.flatten(),
        z=Z.flatten(),
        value=values.flatten(),
        isomin=mind,
        isomax=maxd,
        surface=dict(count=20, fill=0.7, pattern='odd'),
        showscale=False, # remove colorbar
        caps=dict(x_show=True, y_show=False),
        colorscale='Tealgrn',

        ))

    figz.update_layout(
        margin=dict(t=0, l=0, b=0, r =0), # tight layout
        scene_camera_eye=dict(x=1.5, y=1.5, z=1.5),
        paper_bgcolor="#1f2630",
        height = 530,
        scene = dict(
                        xaxis = dict(
                            titlefont_color='white',
                            nticks=6,
                            backgroundcolor="#1f2630",
                            gridcolor="white",
                            showbackground=True,
                            zerolinecolor="#1f2630",
                            tickfont=dict( color='white',)),
                        yaxis = dict(
                            titlefont_color='white',
                            nticks=6,
                            backgroundcolor="#1f2630",
                            gridcolor="white",
                            showbackground=True,
                            zerolinecolor="#1f2630",
                            tickfont=dict( color='white',)),
                        zaxis = dict(
                            titlefont_color='white',
                            nticks=6,
                            backgroundcolor="#1f2630",
                            gridcolor="white",
                            showbackground=True,
                            zerolinecolor="#1f2630",
                            tickfont=dict( color='white',)
                            ),

                        ),)
    figz.update_layout(scene_aspectmode='manual',
                  scene_aspectratio=dict(x=plot_ratio, y=1, z=1))

    return [figz]


if __name__ == "__main__":
    dash_app.run_server(debug=True)