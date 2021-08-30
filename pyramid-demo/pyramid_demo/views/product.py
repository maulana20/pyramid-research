import colander
import deform.widget

from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from pyramid.response import Response
from sqlalchemy.exc import SQLAlchemyError

from .. import models
from .. import enums

class Product:
    def __init__(self, request):
        self.request = request
    
    @property
    def form(self):
        choices = [("", "- Select -")]
        for category in (enums.product.Category): choices.append(category.option())
        
        class Schema(colander.Schema):
            name = colander.SchemaNode(colander.String())
            category = colander.SchemaNode(
                colander.String(),
                widget=deform.widget.SelectWidget(values=choices)
            )
        
        schema = Schema()
        return deform.Form(schema, buttons=('submit',))
    
    @property
    def reqts(self):
        return self.form.get_widget_resources()
    
    @view_config(route_name='product_index', renderer='pyramid_demo:templates/product/index.pt')
    def index(self):
        try:
            products = self.request.dbsession.query(models.Product).filter(models.Product.actived).all()
        except SQLAlchemyError:
            return Response(db_err_msg, content_type='text/plain', status=500)
        return { 'products': products, 'category': enums.product.Category }
    
    @view_config(route_name='product_add', renderer='pyramid_demo:templates/product/add_edit.pt')
    def add(self):
        form = self.form.render()
        
        if 'submit' in self.request.params:
            controls = self.request.POST.items()
            try:
                appstruct = self.form.validate(controls)
            except deform.ValidationFailure as e:
                # Form is NOT valid
                return dict(form=e.render())
            
            # Add a new page to the database
            self.request.dbsession.add(models.Product(name=appstruct['name'], category=appstruct['category']))
            
            url = self.request.route_url('product_index')
            return HTTPFound(url)

        return dict(form=form)
    
    @view_config(route_name='product_edit', renderer='pyramid_demo:templates/product/add_edit.pt')
    def edit(self):
        id = int(self.request.matchdict['id'])
        product = self.request.dbsession.query(models.Product).filter_by(id=id).one()

        form = self.form

        if 'submit' in self.request.params:
            controls = self.request.POST.items()
            try:
                appstruct = form.validate(controls)
            except deform.ValidationFailure as e:
                return dict(page=page, form=e.render())

            # Change the content and redirect to the view
            product.name = appstruct['name']
            product.category = appstruct['category']
            url = self.request.route_url('product_index')
            return HTTPFound(url)

        form = self.form.render(dict(
            id=product.id, name=product.name, category=product.category)
        )

        return dict(product=product, form=form)

db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to initialize your database tables with `alembic`.
    Check your README.txt for descriptions and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
