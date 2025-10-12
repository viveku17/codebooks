import requests
from dash import Dash, dcc, html, Input, Output, callback, State
from src import os_service 
from src import layout_builder


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


app.layout = html.Div(
    children=[
        layout_builder.build_title(),
        layout_builder.build_selection(),
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


# ==========================
# Callbacks
# ==========================


@callback(
    Output("select_repo_status", "value"),
    Output("select_repo_status", "className"),
    Input("select_repo", "value"),
)
def select_repo_action(select_repo_url):
    select_repo_status_value = f"git repo is invalid"
    select_repo_status_class = "input-group-text form-inline w-100 bg-danger"
    if is_valid_git_repo(str(select_repo_url)):
        select_repo_status_value =  "git repo is valid"
        select_repo_status_class = "input-group-text form-inline w-100 bg-success"
    return select_repo_status_value, select_repo_status_class


@callback(
    Output('clone_repo_status', 'value'),
    Output('clone_repo_status', 'className'),
    Output('select_branch', 'options'),
    Input('btn_clone_repo', 'n_clicks'),
    State('select_repo', 'value'),    
    prevent_initial_call=True
)
def clone_repo_action(btn_clone_repo_clicks, select_repo_url):
    clone_repo_status_value = "git repo was not cloned correctly"
    clone_repo_status_class = "input-group-text bg-danger form-inline w-100"
    select_branch_options = []
    if is_valid_git_repo(str(select_repo_url)):
        result = os_service.clone_repo(select_repo_url)
        if result:
            clone_repo_status_value = "git repo was cloned correctly"
            clone_repo_status_class = "input-group-text bg-success form-inline w-100"
            select_branch_options = os_service.get_active_repo_branches()
    return clone_repo_status_value, clone_repo_status_class, select_branch_options


@callback(
    Output('select_branch', 'value'),
    Output('select_branch', 'options', allow_duplicate=True),
    Input('select_branch_filter', 'value'),
    prevent_initial_call=True,
)
def select_branch_filter_action(select_branch_filter_value):
    branch_filter = select_branch_filter_value.strip().lower()
    branches = os_service.get_active_repo_branches()
    select_branch_value = ""
    select_branch_options = [option for option in branches if option.lower().startswith(branch_filter)]
    if select_branch_options:
         select_branch_value = select_branch_options[0]
    return select_branch_value, select_branch_options


@callback(
    Output('checkout_branch_status', 'value'),
    Output('checkout_branch_status', 'className'),
    Input('btn_checkout_branch', 'n_clicks'),
)
def checkout_branch_action(btn_checkout_branch_clicks):
    pass
    # clone_repo_status_value = "git repo was not cloned correctly"
    # clone_repo_status_class = "input-group-text bg-danger form-inline w-100"
    # select_branch_options = []
    # if is_valid_git_repo(str(select_repo_url)):
    #     result = os_service.clone_repo(select_repo_url)
    #     if result:
    #         clone_repo_status_value = "git repo was cloned correctly"
    #         clone_repo_status_class = "input-group-text bg-success form-inline w-100"
    #         select_branch_options = os_service.get_active_repo_branches()
    # return clone_repo_status_value, clone_repo_status_class, select_branch_options



# ==========================
# Private Methods
# ==========================


def is_valid_git_repo(url):
    if (url.startswith("https://") and url.endswith(".git")):
        try:
            response = requests.get(url)
            if response:
                return (response.status_code == 200)
        except:
            pass
    return False        

