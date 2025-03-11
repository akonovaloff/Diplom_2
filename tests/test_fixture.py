from conftest import new_user, existing_user, not_valid_pass_user, generate_new_user


class TestFixture:

    def test_fixture_new_user(self, new_user):
        pass

    def test_fixture_existed_user(self, existing_user):
        pass

    def test_fixture_not_valid_pass_user(self, not_valid_pass_user):
        pass

    def test_generate_new_user(self, generate_new_user):
        print(generate_new_user())
        print(generate_new_user())