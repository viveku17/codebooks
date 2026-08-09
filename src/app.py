from dash import Dash

from src.model.repository_model import RepositoryModel
from src.data_provider.git_repo_data_provider import GitRepoDataProvider
from src.view.dashboard_view import DashboardView
from src.view_presenter.dashboard_presenter import DashboardPresenter


model = RepositoryModel()
provider = GitRepoDataProvider(model)
view = DashboardView()
presenter = DashboardPresenter(view, provider)

app = Dash(__name__)
app.layout = presenter.get_layout()


if __name__ == "__main__":
    app.run(debug=True)
