def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('product_index', '/product')
    config.add_route('product_add', '/product/add')
    config.add_route('product_edit', '/product/{id}/edit')
