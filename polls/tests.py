from django.test import TestCase
from .models import Question
from django.urls import reverse
from django.utils import timezone
import datetime

def create_question(question_text,pub_date):
	return Question.objects.create(question_text=question_text,pub_date=pub_date)

class QuestionModelTest(TestCase):
	def test_was_published_recently_with_future_questions(self):
		future_question=create_question('test question',timezone.now()+datetime.timedelta(days=30))
		self.assertIs(future_question.was_published_recently(),False)

	def test_was_published_recently_with_old_questions(self):
		old_question=create_question('test question',timezone.now()-datetime.timedelta(days=30))
		self.assertIs(old_question.was_published_recently(),False)

	def test_was_published_recently_with_recent_questions(self):
		recent_question=create_question('test question',timezone.now()-datetime.timedelta(days=0.5))
		self.assertIs(recent_question.was_published_recently(),True)

class PollsIndexViewTest(TestCase):
	def test_no_questions(self):
		response=self.client.get(reverse("polls:index"))
		self.assertEqual(response.status_code,200)
		self.assertContains(response,"No polls are available")

	def test_past_question(self):
		past_question=create_question('test question',timezone.now()-datetime.timedelta(days=0.5))
		response=self.client.get(reverse("polls:index"))
		self.assertQuerysetEqual(response.context['latest_question_list'],[past_question])

	def test_future_question(self):
		future_question=create_question('test question',timezone.now()+datetime.timedelta(days=1))
		response=self.client.get(reverse("polls:index"))
		self.assertContains(response,"No polls are available")

	def test_future_question_and_past_question(self):
		past_question=create_question('test question',timezone.now()-datetime.timedelta(days=0.5))
		future_question=create_question('test question',timezone.now()+datetime.timedelta(days=1))
		response=self.client.get(reverse("polls:index"))
		self.assertQuerysetEqual(response.context['latest_question_list'],[past_question])

	def test_two_past_questions(self):
		past_question1=create_question('test question 1',timezone.now()-datetime.timedelta(days=0.5))
		past_question2=create_question('test question 2',timezone.now()-datetime.timedelta(days=0.5))
		response=self.client.get(reverse("polls:index"))
		self.assertQuerysetEqual(response.context['latest_question_list'],[past_question1,past_question2])

class PollsDetailViewTest(TestCase):
	def test_future_question(self):
		future_question=create_question("test question",timezone.now()+datetime.timedelta(days=1))
		response=self.client.get(reverse("polls:detail",args=(future_question.id,)))
		self.assertEqual(response.status_code,404)

	def test_past_question(self):
		past_question=create_question("test question",timezone.now()-datetime.timedelta(days=1))
		response=self.client.get(reverse("polls:detail",args=(past_question.id,)))
		self.assertContains(response,past_question.question_text)
