import json
from django.test import TestCase
from django.core.urlresolvers import reverse


class IndexViewTests(TestCase):
    def test_returns_ok(self):
        resp = self.client.get(reverse('api_index'))
        self.assertEqual(resp.status_code, 200)
        status = json.loads(resp.content).get('status')
        self.assertEqual(status, "OK")
