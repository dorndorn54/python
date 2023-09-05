import unittest
import python_repos as pr


class PythonReposTestCase(unittest.TestCase):
    # test for test_python_repos.py

    def setUp(self):
        # call all functions and test separately
        self.r = pr.get_response()
        self.repo_dicts = pr.get_repo_dicts(self.r)
        self.repo_dict = self.repo_dicts[0]
        self.names, self.plot_dicts = pr.get_names_plot_dicts(self.repo_dicts)

    def test_get_response(self):
        # the return code should be 200
        self.assertEqual(self.r.status_code, 200)

    def test_get_repo_dicts(self):
        self.assertEqual(len(self.repo_dicts), 30)

        required_keys = ['name', 'owner', 'stargazers_count', "html_url"]
        for key in required_keys:
            self.assertIn(key, self.repo_dict.keys())


unittest.main()
