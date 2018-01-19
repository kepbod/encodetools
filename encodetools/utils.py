def fetch_attr(obj, info, json, dict):
    for entry in info:
        attr, attrname, desc = entry
        if attr in json:
            # extract attribute
            setattr(obj, attrname, json[attr])
            # update dictionary
            dict[attrname] = desc
