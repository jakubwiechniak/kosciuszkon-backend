def success(data):
    return {
        "success": True,
        "data": data
    }


def failed(data):
    return {
        "success": False,
        "data": data
    }
