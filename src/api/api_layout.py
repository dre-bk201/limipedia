
# {<insert here>} --> means an option out of a list
resources = ["monsters", "weapons", "defgears"]

# https://www.limipedia.com/api/v1/{resource} - return all ids
# https://www.limipedia.com/api/v1/{resource}?search=Kagu - return all ids
# https://www.limipedia.com/api/v1/{resource}/[id] - return a specific monster by id
# https://www.limipedia.com/api/v1/{resource}/[id]/[name] - return a specific monster name
# https://www.limipedia.com/api/v1/{resource}/[id]/basicInfo - return a specific monster by i
# https://www.limipedia.com/api/v1/{resource}/[id]?limit=100/ - return a specific monster by id
# https://www.limipedia.com/api/v1/{resource}/gear_cost/[cost]?gt=[int] - return a specific monster by id


"""
--------- QUERY PARAMS ---------
features:
    - limits (limit)
    - pagination (offset)
    - sorting (sort=name_asc) (asc, desc)
    - partial comparison (gt, lt)
    - search (?search=Kagu)
"""