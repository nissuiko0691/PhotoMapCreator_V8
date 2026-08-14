from pathlib import Path


class ProjectManager:

    def __init__(self, root_dir):

        self.root = Path(root_dir)

        self.projects_dir = self.root / "projects"

        self.projects_dir.mkdir(exist_ok=True)

    # -----------------------------------------
    # プロジェクト一覧取得
    # -----------------------------------------
    def get_projects(self):

        projects = []

        for p in self.projects_dir.iterdir():

            if p.is_dir():

                projects.append(p.name)

        projects.sort()

        return projects

    # -----------------------------------------
    # 新規プロジェクト作成
    # -----------------------------------------
    def create_project(self, name):

        project = self.projects_dir / name

        project.mkdir(exist_ok=True)

        (project / "photos").mkdir(exist_ok=True)

        (project / "output").mkdir(exist_ok=True)

        return project

    # -----------------------------------------
    # プロジェクトを開く
    # -----------------------------------------
    def open_project(self, name):

        return self.projects_dir / name