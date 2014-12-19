from django.test import TestCase

from peacecorps.models import FAQ


class BraveSirTrevorTest(TestCase):
    def test_no_explosion(self):
        """Verify that we don't blow up when the field is improperly
        formatted"""
        faq = FAQ.objects.create(question='uniq', answer=None)
        self.assertEqual(FAQ.objects.get(question='uniq').answer.html, '')
        faq.answer = ''
        faq.save()
        self.assertEqual(FAQ.objects.get(question='uniq').answer.html, '')
        faq.answer = 'Some non-json'
        faq.save()
        answer = FAQ.objects.get(question='uniq').answer.html
        self.assertTrue('Some non-json' in answer)
        self.assertTrue('DATA FORMAT INCORRECT' in answer)
        faq.delete()
