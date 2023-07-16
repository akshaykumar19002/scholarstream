from decimal import Decimal
import copy

from course.models import Course

class Cart:

    def __init__(self, request) -> None:
        self.session = request.session
        cart = self.session.get('session-key')

        if 'session-key' not in request.session:
            cart = self.session['session-key'] = {}

        self.cart = cart
        
    def clear(self):
        del self.session['session-key']
        self.session.modified = True

    def add(self, course):
        course_id = str(course.id)
        self.cart[course_id] = {'price': str(course.price)}
        self.session.modified = True

    def delete(self, course_id):
        course_id = str(course_id)

        if course_id in self.cart:
            del self.cart[course_id]
            self.session.modified = True

    def __len__(self):
        return len([course_id for course_id in self.cart.keys()])
    
    def __iter__(self):
        course_ids = self.cart.keys()
        courses = Course.objects.filter(id__in=course_ids)

        cart = copy.deepcopy(self.cart)

        for course in courses:
            cart[str(course.id)]['course'] = course

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            yield item

    def get_total_price(self):
        return sum(int(course['price']) for course in self.cart.values())
    
    def exists(self, course):
        for item in self.cart.values():
            if course == item['course']:
                return True
        return False
    
    def __neq__(self, course):
        for item in self.cart.values():
            if course == item['course']:
                return False
        return True