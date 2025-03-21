from marshmallow import Schema, fields
 
# class ItemSchema(Schema):
class PlainItemSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    # store_id = fields.Str(required=True)
   
# class StoreSchema(Schema):
class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
 
class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
 
class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()
    store_id=fields.Int()
 
 
class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(),dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()),dump_only=True)
# //response
class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only= True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only= True)
 
 
class TagSchema(PlainTagSchema):
    store_id = fields.Int(load_only=True)
    store = fields.Nested(PlainStoreSchema(),dump_only=True)
    items = fields.List(fields.Nested(PlainItemSchema()),dump_only=True)  
 
class TagAndItemSchema(Schema):
    message=fields.Str()
    item=fields.Nested(ItemSchema)
    tag=fields.Nested(TagSchema)


class UserSchema(Schema):
    id = fields.Int(dump_only=True)  # The 'id' is read-only in responses (dump_only)
    username = fields.Str(required=True)  # 'username' is required
    password = fields.Str(required=True, load_only=True)  # 'password' is required for input but not included in the output
