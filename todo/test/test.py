import unittest
from app import app
from app.models import Todo


class TodoTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        todos = Todo.objects.all()
        for todo in todos:
            todo.delete()

    def test_index(self):
        res = self.app.get('/')
        assert "Todo" in res.data

    def test_add(self):
        self.app.post('/add', data=dict(content="Test add"))
        todo = Todo.objects.get_or_404(content="Test add")
        assert todo is not None
