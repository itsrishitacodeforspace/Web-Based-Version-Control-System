import unittest
from server.vcs import VersionControlSystem

class TestVersionControlSystem(unittest.TestCase):
    def setUp(self):
        # Create an instance of the version control system
        self.vcs = VersionControlSystem()

    def test_commit_on_main_branch(self):
        files = {
            "index.html": "<html><body>Hello World</body></html>",
            "style.css": "body { color: blue; }"
        }
        commit1 = self.vcs.commit("Initial commit on main branch", files)
        self.assertEqual(commit1.message, "Initial commit on main branch")
        self.assertIn("index.html", commit1.files)

    def test_branch_creation_and_commit(self):
        self.vcs.create_branch("feature-branch")
        self.vcs.switch_branch("feature-branch")

        files = {
            "index.html": "<html><body>Feature update!</body></html>",
            "style.css": "body { color: green; }"
        }
        commit2 = self.vcs.commit("Commit on feature branch", files)
        self.assertEqual(commit2.message, "Commit on feature branch")
        self.assertEqual(self.vcs.current_branch, "feature-branch")

    def test_merge_branch(self):
        # Commit on main branch
        files_main = {
            "index.html": "<html><body>Hello World</body></html>",
            "style.css": "body { color: blue; }"
        }
        self.vcs.commit("Initial commit on main branch", files_main)

        # Create and switch to feature branch
        self.vcs.create_branch("feature-branch")
        self.vcs.switch_branch("feature-branch")

        files_feature = {
            "index.html": "<html><body>Feature update!</body></html>",
            "style.css": "body { color: green; }"
        }
        self.vcs.commit("Commit on feature branch", files_feature)

        # Merge feature branch into main
        self.vcs.switch_branch("main")
        merge_result = self.vcs.merge_branch("feature-branch")

        # Check if there are conflicts
        if merge_result['conflicts']:
            self.assertListEqual(merge_result['conflicts'], ["style.css", "index.html"])
        else:
            self.assertIn("commit", merge_result)
            self.assertFalse(merge_result['conflicts'])

    def test_switch_back(self):
        self.vcs.create_branch("feature-branch")
        self.vcs.switch_branch("feature-branch")
        self.vcs.switch_back()
        self.assertEqual(self.vcs.current_branch, "main")

    def test_switch_to_non_existent_branch(self):
        with self.assertRaises(ValueError):
            self.vcs.switch_branch("non-existent-branch")

if __name__ == "__main__":
    unittest.main()
