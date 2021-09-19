import requests


def get_catalog(max_try_quantity=5):
    catalog_url = 'https://poshmark.com/vm-rest/meta/catalog_v2?pm_version=163.0.0'
    response = requests.get(catalog_url)
    try_quantity = 0

    while response.status_code != 200:
        if try_quantity < max_try_quantity:
            response = requests.get(catalog_url)
        else:
            return False
    data = response.json()
    return data


def get_catalog_display(max_try_quantity=5, country="us"):
    catalog_url = 'https://poshmark.com/vm-rest/meta/catalog_display?pm_version=163.0.0'
    response = requests.get(catalog_url)
    try_quantity = 0

    while response.status_code != 200:
        if try_quantity < max_try_quantity:
            response = requests.get(catalog_url)
        else:
            return False
    data = response.json()
    return data.get("data").get(country).get("catalog_display").get("children")


def get_categories_by_departments(departments):
    categories_dict = {}
    for department in departments:
        department_name = department.get('display')
        department_id = department.get('id')
        category_dict = {"name": department_name, 'data': {}}

        for category in department.get('categories'):
            category_id = category.get("id")
            category_dict['data'][category_id] = {
                "name": category.get("display"), 'data': {}}
            sub_index = 0
            if not category.get("category_features"):
                continue

            for feature in category.get("category_features"):
                feature_name = feature.get("display")

                feature_data = {
                    "id": feature.get("id"),
                    "index": sub_index,
                    "feature_name": feature_name
                }
                category_dict['data'][category_id]["data"][feature_name] = feature_data
                sub_index = sub_index + 1

        categories_dict[department_id] = category_dict

    return categories_dict


def get_sub_categories_by_department(department, categories):
    category_dict = {}
    index = 0
    for children in categories:
        if children.get("type") == 'category':
            catalog_data = department.get("data").get(children.get("id"))
            category = {
                "index": index,
                "children": catalog_data.get("data")
            }
            category_dict[catalog_data.get("name")] = category

        else:
            data = get_sub_categories_by_department(
                department, children.get('children'))
            category_dict[children.get("display")] = data

        index = index + 1

    return category_dict


def get_categories(departments_data, catalog_display_data):
    category_dict = {}
    for department_data in catalog_display_data:
        department_id = department_data.get("id")
        department = departments_data.get(department_id)
        department_name = department.get("name")
        category_dict[department_name] = get_sub_categories_by_department(
            department, department_data.get("children"))

    return category_dict


def get_category_dict():
    catalog = get_catalog()
    catalog_display_data = get_catalog_display()
    departments_data = get_categories_by_departments(
        catalog.get('catalog').get('departments'))
    category_dict = get_categories(departments_data, catalog_display_data)
    return category_dict
