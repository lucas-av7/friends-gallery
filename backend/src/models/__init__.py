from mongoengine import Document, fields, CASCADE, NULLIFY


class User(Document):
    name = fields.StringField(required=True)
    email = fields.EmailField(required=True, unique=True)
    password = fields.StringField(required=True, min_length=8)
    is_admin = fields.BooleanField(required=True, default=False)

    def to_dict(self):
        data = self.to_mongo()
        del data["password"]
        return data


class Photo(Document):
    approved = fields.BooleanField(default=False)
    likes = fields.ListField(fields.StringField())
    title = fields.StringField(max_length=100, default="Untitled photo")
    url = fields.URLField(required=True)
    delete_key = fields.StringField(required=True)
    user = fields.ReferenceField(User, required=True, reverse_delete_rule=NULLIFY)

    def to_dict(self):
        data = self.to_mongo()
        if "user" in data:
            data["user"] = {"name": self.user.name, "_id": self.user.id}
        return data


class Comment(Document):
    content = fields.StringField(max_length=250, required=True)
    likes = fields.ListField(fields.StringField())
    user = fields.ReferenceField(User, required=True, reverse_delete_rule=CASCADE)
    photo = fields.ReferenceField(Photo, required=True, reverse_delete_rule=CASCADE)

    def to_dict(self):
        data = self.to_mongo()
        data["user"] = {"name": self.user.name, "_id": self.user.id}
        del data["photo"]
        return data
