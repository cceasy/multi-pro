import traceback

def internal_server(error):
    return traceback.format_exc(), 500

def page_not_found(error):
    return 'Not Found', 404

error_handlers = {
    404: page_not_found,
    500: internal_server
}