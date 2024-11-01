from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from datetime import datetime

# Data contoh menu kafe yang lebih lengkap
cafe_menu = [
    {"id": "1", "name": "Cappuccino", "description": "Rich and creamy coffee with frothy milk.", "price": 50000},
    {"id": "2", "name": "Latte", "description": "Smooth espresso with steamed milk.", "price": 55000},
    {"id": "3", "name": "Cheesecake", "description": "Delicious cheesecake with a graham cracker crust.", "price": 75000},
    {"id": "4", "name": "Caesar Salad", "description": "Crisp romaine lettuce with Caesar dressing.", "price": 60000},
    {"id": "5", "name": "Chocolate Cake", "description": "Rich and moist chocolate cake.", "price": 70000},
    {"id": "6", "name": "Herbal Tea", "description": "Refreshing blend of herbal flavors.", "price": 30000},
]

# Detail menu yang lebih lengkap
menu_details = {item['id']: item for item in cafe_menu}

app = Flask(__name__)
api = Api(app)

class MenuList(Resource):
    def get(self):
        return {
            "error": False,
            "message": "success",
            "count": len(cafe_menu),
            "menu": cafe_menu
        }

class MenuDetail(Resource):
    def get(self, menu_id):
        if menu_id in menu_details:
            return {
                "error": False,
                "message": "success",
                "menu": menu_details[menu_id]
            }
        return {"error": True, "message": "Menu item not found"}, 404

class AddMenu(Resource):
    def post(self):
        data = request.get_json()
        new_item = {
            "id": str(len(cafe_menu) + 1),  # Generate a new ID
            "name": data.get('name'),
            "description": data.get('description'),
            "price": data.get('price')
        }
        cafe_menu.append(new_item)
        menu_details[new_item['id']] = new_item
        return {
            "error": False,
            "message": "Menu item added successfully",
            "menu": new_item
        }, 201

class UpdateMenu(Resource):
    def put(self, menu_id):
        data = request.get_json()
        if menu_id in menu_details:
            item_to_update = menu_details[menu_id]
            item_to_update['name'] = data.get('name', item_to_update['name'])
            item_to_update['description'] = data.get('description', item_to_update['description'])
            item_to_update['price'] = data.get('price', item_to_update['price'])
            return {
                "error": False,
                "message": "Menu item updated successfully",
                "menu": item_to_update
            }
        return {"error": True, "message": "Menu item not found"}, 404

class DeleteMenu(Resource):
    def delete(self, menu_id):
        if menu_id in menu_details:
            cafe_menu.remove(menu_details[menu_id])
            del menu_details[menu_id]
            return {
                "error": False,
                "message": "Menu item deleted successfully"
            }
        return {"error": True, "message": "Menu item not found"}, 404

# Menambahkan resource ke API
api.add_resource(MenuList, '/menu')
api.add_resource(MenuDetail, '/menu/<string:menu_id>')
api.add_resource(AddMenu, '/menu/add')
api.add_resource(UpdateMenu, '/menu/update/<string:menu_id>')
api.add_resource(DeleteMenu, '/menu/delete/<string:menu_id>')

if __name__ == '__main__':
    app.run(debug=True)
