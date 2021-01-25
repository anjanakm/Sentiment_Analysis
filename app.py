import pickle
import pandas as pd
import dash
import webbrowser
import dash_html_components as html
import webbrowser
from dash.dependencies import Input, Output,State
import dash_core_components as dcc
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import plotly.express as px
import plotly.graph_objs as go

app = dash.Dash()
project_name = None

with open("df1_pickel.pkl", 'rb') as file:
   df1 = pickle.load(file)
   df1=df1.reset_index(drop=True)
   
def load_model():
    global df,pos,neg
    pos = 0
    neg = 0
    df = pd.read_csv('balanced_reviews.csv')
    
   
    for i in range(0,527378):
        if(df1['Positivity'][i] == 1):
            pos+=1
        else:
            neg+=1
            
    global pickle_model
    file = open("pickle_model.pkl", 'rb')
    pickle_model = pickle.load(file)
    
    global vocab
    file = open("feature.pkl" , 'rb')
    vocab = pickle.load(file)
    
    
def check_review(reviewText):
    
    transformer = TfidfTransformer()
    loaded_vec = CountVectorizer(decode_error="replace",vocabulary=pickle.load(open("feature.pkl","rb")))
    reviewText = transformer.fit_transform(loaded_vec.fit_transform([reviewText]))
    
    return pickle_model.predict(reviewText)

def open_browser():
    webbrowser.open_new('http://127.0.0.1:8050/')
    
data=pd.read_csv("balanced_reviews.csv")
etsy = pd.read_csv("reviews_etsy.csv")
labels = ['Positive','Negative']



def get_options(list):
    dict=[]
    for i in list:
        dict.append({'label':i, 'value':i})
    return dict

    



def create_app_ui():
    # Create the UI of the Webpage here
    main_layout = html.Div(
    [
     
     html.H1(children='Sentiments Analysis with Insights', id='Main_title',style={'text-align':'center','fontsize':60}),
     html.Div(style={'backgroundColor':'yellow'},children=[
            html.H3(children='Review Pie Chart', id='sub_heading1',style={'color':'black','fontSize':30,'text-align':'center'}),
            dcc.Graph(figure=px.pie(df1,values=[pos,neg],names=['Positive Reviews','Negative Reviews'],opacity=1,color_discrete_map=('Red','Green')))
            ], className='piegraph'),
     html.Div(style={'backgroundColor':'yellow'}, children=[
        html.Div([
            html.H3(children='Check reviews from dropdown', id='sub_heading2',style={'color':'#0A0865','fontSize':20,'text-align':'center'}),
     dcc.Dropdown(id='drop',options=get_options(etsy['review'][0:134]) ,value=[etsy['review'].sort_values()[0]],className='Review Selector'),
     html.Button(id='button1',children='Search',n_clicks=0,style={'backgroundColor':'cyan','text-align':'center','fontSize':20}),
     html.H1(children=None, id='result1',style={'width': '100%','color':'851C06','text-align':'center'}),
        ],className='Dropdown'),
        html.Div([
            html.H3(children='Enter review below', id='sub_heading3',style={'color':'#0A0865','fontSize':20,'text-align':'center'}),
     dcc.Textarea(
        id='textarea_review',
        placeholder='Enter the review here...',
        style={'width': '100%', 'height': 100}
        ),
      
      html.Button(id='button',children='Search',n_clicks=0,style={'backgroundColor':'cyan','text-align':'center','fontSize':20}),
      html.H1(children=None, id='result',style={'color':'851C06','text-align':'center'}),
            
        ], className='textreview')
      
    ])
     ],className='main')
    
    return main_layout

@app.callback(
    Output('result', 'children'),
    
    [
    Input('textarea_review', 'value'),
    Input('button','n_clicks'),
    
    ])

def update_app_ui(textarea_value,n_clicks):
    print("Data Type  = ", str(type(textarea_value)))
    print("Value      = ", str(textarea_value))
   
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    result_list = check_review(textarea_value)
    
    
    
    if 'button' in changed_id:
        
        if (result_list[0] == 0 ):
            result = 'Negative'
        elif (result_list[0] == 1):
            result = 'Positive'
        else:
            result = 'Unknown'
    
    
    return result

@app.callback(
    Output('result1','children'),
    [
     Input('button1','n_clicks'),
     Input('drop','value')
     ])

def update_app_ui_1(n_clicks,value):
    print("Data Type  = ", str(type(value)))
    print("Value      = ", str(value))
   
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    result_list1 = check_review(value)
    
    
    if 'button1' in changed_id:
        
        if (result_list1[0] == 0 ):
            result1 = 'Negative'
        elif (result_list1[0] == 1):
            result1 = 'Positive'
        else:
            result1 = 'Unknown'
    
    return result1
def main():
    load_model()
    open_browser()
    
    
    
    global project_name
    project_name = 'Sentiments Analysis with Insights'
    
    global app
    app.title= project_name
    
    app.layout = create_app_ui()
   
    app.run_server()  #infinite loop
    
   
    app = None
    project_name = None
    
    
    
    
if __name__ == '__main__':
    main()