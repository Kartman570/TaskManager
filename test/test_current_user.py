from test.base import TestViewSetBase
from main.serializers import UserSerializer


class TestUserViewSet(TestViewSetBase):
    basename = "current_user"

    def test_retrieve(self):
        user = self.single_resource()
        serializer = UserSerializer(self.user)
        user_dict = serializer.data
        user_dict["avatar_picture"] = "http://testserver" + user_dict["avatar_picture"]
        assert user == user_dict

    def test_patch(self):
        self.patch_single_resource({"first_name": "TestName"})

        user = self.single_resource()
        assert user["first_name"] == "TestName"
