import requests
from dash import Dash, dcc, html, Input, Output, callback, ctx, State
from src import os_service 


JS_LIST = [
    {
        "src": "https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js",
        "integrity": "sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL",
        "crossorigin": "anonymous"
    }
]

CSS_LIST = [
    {
        "href": "https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css",
        'rel': 'stylesheet',
        "integrity": "sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN",
        "crossorigin": "anonymous"
    }
]

app = Dash(__name__,
           external_scripts=JS_LIST,
           external_stylesheets=CSS_LIST)


def build_title():
    return html.H1(children="CodeBooks", className="text-primary")


def build_selection():
    return html.Div(
        children=[
            html.H3(children="Selection"),
            build_selection_select_repo(),
            build_selection_clone_repo(),
            build_selection_select_branch(),
            build_selection_checkout_branch()
        ],
        className="p-3"
    )


def build_selection_select_repo():
    return html.Div(
        children=[
            html.Div(
                children=[
                    dcc.Input(id="select_repo", type="url", placeholder="url to git repo",
                              className="form-control w-100"),
                ],
                className="col"
            ),
            html.Div(
                children=[
                    dcc.Input(id="select_repo_status", type="text", readOnly=True, 
                              className="input-group-text bg-danger form-inline w-100"),
                ],
                className="col"
            )
        ],
        className="row mt-2"
    )

def build_selection_clone_repo():
    return html.Div(
        children=[
            html.Div(
                children=[
                    html.Button('Clone Repo', id='btn_clone_repo', className="btn btn-primary w-100")
                ],
                className="col"
            ),
            html.Div(
                children=[
                    dcc.Input(id="clone_repo_status", type="text", readOnly=True, 
                              className="input-group-text bg-danger form-inline w-100"),
                ],
                className="col"
            )
        ],
        className="row mt-2"
    )


def build_selection_select_branch():
    return html.Div(
        children=[
            html.Div(
                children=[
                    dcc.Dropdown(["main"], "main", id="select_branch"),
                ],
                className="col"
            ),
            html.Div(
                children=[
                    html.Div(
                        children=[
                            html.Span(children=["Select Branch Filter"], className="input-group-text")
                        ],
                        className="input-group-prepend col w-25"
                    ),
                    dcc.Input(id="select_branch_filter", type="text", placeholder="", 
                              className="form-control w-75"),
                ],
                className="input-group col"
            )
        ],
        className="row mt-2"
    )


def build_selection_checkout_branch():
    return html.Div(
        children=[
            html.Div(
                children=[
                    html.Button('Checkout Branch', id='btn_checkout_branch', className="btn btn-primary w-100")
                ],
                className="col"
            ),
            html.Div(
                children=[
                    dcc.Input(id="checkout_branch_status", type="text", readOnly=True, 
                              className="input-group-text bg-danger form-inline w-100"),
                ],
                className="col"
            )
        ],
        className="row mt-2"
    )


app.layout = html.Div(
    children=[
        build_title(),
        build_selection(),
        html.Div(
            children=[
                html.H3(children="Status")
            ],
            className="p-3"
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.H3(children="Commits")
                    ],
                    className="col"
                ),
                html.Div(
                    children=[
                        html.H3(children="Files")
                    ],
                    className="col"
                ),
                html.Div(
                    children=[
                        html.H3(children="Content")
                    ],
                    className="col-6"
                )
            ],
            className="row p-3"
        ),
    ],
    className="p-3 container"
)


@callback(
    Output("select_repo_status", "value"),
    Output("select_repo_status", "className"),
    Input("select_repo", "value"),
)
def update_repo_selection_status(select_repo_url):
    select_repo_status_value = f"git repo is invalid"
    select_repo_status_class = "input-group-text form-inline w-100 bg-danger"
    if is_valid_git_repo(str(select_repo_url)):
        select_repo_status_value =  "git repo is valid"
        select_repo_status_class = "input-group-text form-inline w-100 bg-success"
    return select_repo_status_value, select_repo_status_class


def is_valid_git_repo(url):
    if (url.startswith("https://") and url.endswith(".git")):
        try:
            response = requests.get(url)
            if response:
                return (response.status_code == 200)
        except:
            pass
    return False        


@callback(
    Output('clone_repo_status', 'value'),
    Input('btn_clone_repo', 'n_clicks'),
    State('select_repo', 'value'),    
    prevent_initial_call=True
)
def clone_repo_and_update_status(btn_clone_repo_clicks, select_repo_url):
    if is_valid_git_repo(str(select_repo_url)):
        os_service.clone_repo(select_repo_url)
