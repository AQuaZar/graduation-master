from django.test import TestCase
from .models import TestQuestion, User, Tutor, Course, TestPackage
from django.core.files.uploadedfile import SimpleUploadedFile
import os
# Create your tests here.


class QuestionsTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username="test-user", password="test123")
        image = SimpleUploadedFile(name='test_image.jpg',
                                   content=open(os.path.abspath("lms_app/anon.jpeg"), 'rb').read(),
                                   content_type='image/jpeg')
        tutor = Tutor.objects.create(user=user, photo=image, position="Proff.", email="testmail@gmail.com")
        package = TestPackage.objects.create(name="TestPack1", created_by=tutor)
        TestQuestion.objects.create(test_package=package,
                                    question="What does the fox say?",
                                    answer_variants="The he hee. Awwuuu Awuuu. Hatee-hatee-hatee-ho!",
                                    answer="Hatee-hatee-hatee-ho!")

    def test_question(self):
        question = TestQuestion.objects.get(id=1)
        self.assertEqual(question.variants_list, ['The he hee.', 'Awwuuu Awuuu.', 'Hatee-hatee-hatee-ho!'])
        self.assertEqual(question.is_correct_answer("Whaa"), False)
        self.assertEqual(question.is_correct_answer("Hatee-hatee-hatee-ho!"), True)




