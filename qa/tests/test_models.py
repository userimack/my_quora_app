from django.contrib.auth.models import User
import pytest

from qa.models import Question


@pytest.mark.django_db
class TestDatabaseOperation():
    def setup(self):
        self.user = User(username="test", password="test123")
        self.user.save()
        self.question = Question(subject="Test Question",
                                 description="", contributor=self.user)
        self.question.save()

    def teardown(self):
        self.question.delete()
        self.user.delete()

    def test_question_contibutor(self):
        assert self.user == self.question.contributor

    # upvotes
    def test_question_upvote_when_no_upvotes_are_present(self):
        self.question.upvote(self.user)
        assert self.user in self.question.upvoted_by_users.all()

    def test_question_upvotes_count_when_no_upvotes_are_present(self):
        self.question.upvote(self.user)
        assert self.question.total_upvotes == 1

    def test_question_upvotes_count_when_a_user_has_already_upvoted(self):
        self.question.upvote(self.user)
        self.question.upvote(self.user)
        assert self.question.total_upvotes == 1

    def test_question_upvotes_count_when_a_user_upvotes_and_upvotes_are_present(self):
        self.user1 = User(username="test1", password="test123")
        self.user1.save()
        self.question.upvote(self.user1)
        self.question.upvote(self.user)
        self.user1.delete()
        assert self.question.total_upvotes == 2

    def test_question_downvotes_count_when_a_user_upvotes_and_no_upvotes_are_present(self):
        old_total_downvotes_count = self.question.total_downvotes
        self.question.upvote(self.user)
        assert self.question.total_downvotes == old_total_downvotes_count

    def test_question_downvotes_count_when_a_user_upvotes_and_upvotes_are_present(self):
        old_total_downvotes_count = self.question.total_downvotes
        self.user1 = User(username="test1", password="test123")
        self.user1.save()
        self.question.upvote(self.user1)
        self.question.upvote(self.user)
        assert self.question.total_downvotes == old_total_downvotes_count

    def test_question_upvotes_count_when_a_user_downvotes_and_upvotes(self):
        self.question.downvote(self.user)
        self.question.upvote(self.user)
        assert self.question.total_upvotes == 1

    def test_question_downvotes_count_when_a_user_downvotes_and_upvotes(self):
        self.question.downvote(self.user)
        self.question.upvote(self.user)
        assert self.question.total_downvotes == 0

    def test_question_upvotes_count_when_a_user_upvotes_and_downvotes(self):
        self.question.upvote(self.user)
        self.question.downvote(self.user)
        assert self.question.total_upvotes == 0

    def test_question_downvotes_count_when_a_user_upvotes_and_downvotes(self):
        self.question.upvote(self.user)
        self.question.downvote(self.user)
        assert self.question.total_downvotes == 1

    def test_question_when_user_upvotes_twice(self):
        self.question.upvote(self.user)
        self.question.upvote(self.user)
        assert self.question.total_upvotes == 1

    # downvotes
    def test_question_downvote_when_no_downvotes_are_present(self):
        self.question.downvote(self.user)
        assert self.user in self.question.downvoted_by_users.all()

    def test_question_downvotes_count_when_a_user_downvotes_and_no_downvotes_are_present(self):
        self.question.downvote(self.user)
        assert self.question.total_downvotes == 1

    def test_question_downvotes_count_when_a_user_downvotes_and_downvotes_are_present(self):
        self.user1 = User(username="test1", password="test123")
        self.user1.save()
        self.question.downvote(self.user1)
        self.question.downvote(self.user)
        assert self.question.total_downvotes == 2

    def test_question_upvotes_count_when_a_user_downvotes_and_no_downvotes_are_present(self):
        old_total_upvotes_count = self.question.total_upvotes
        self.question.downvote(self.user)
        assert self.question.total_upvotes == old_total_upvotes_count

    def test_question_upvotes_count_when_a_user_downvotes_and_downvotes_are_present(self):
        old_total_upvotes_count = self.question.total_upvotes
        self.user1 = User(username="test1", password="test123")
        self.user1.save()
        self.question.downvote(self.user1)
        self.question.downvote(self.user)
        assert self.question.total_upvotes == old_total_upvotes_count

    def test_question_when_user_downvotes_twice(self):
        self.question.downvote(self.user)
        self.question.downvote(self.user)
        assert self.question.total_downvotes == 1

    # testing has_upvoted / has_downvoted
    def test_question_has_upvoted_when_user_has_not_upvoted(self):
        assert not self.question.has_upvoted(self.user)

    def test_question_has_upvoted_when_user_has_already_upvoted(self):
        self.question.upvote(self.user)
        assert self.question.has_upvoted(self.user)

    def test_question_has_downvoted_when_user_has_not_downvoted(self):
        assert not self.question.has_downvoted(self.user)

    def test_question_has_downvoted_when_user_has_already_downvoted(self):
        self.question.downvote(self.user)
        assert self.question.has_downvoted(self.user)
