from cats_db import CatDatabase

if __name__ == '__main__':
    cat_db = CatDatabase('cats')

    # Inserting a new cat
    cat_id = cat_db.insert_cat('barsik', 3, ['likes to sleep', 'enjoys cuddles'])
    print(f'Inserted cat with id {cat_id}')

    # Inserting a second cat
    cat_id = cat_db.insert_cat('Tom', 1000, ['like mouses'])
    print(f'Inserted cat with id {cat_id}')

    # Finding and displaying all cats
    print('All cats in the database:')
    all_cats = cat_db.find_all_cats()
    for cat in all_cats:
        print(cat)

    # Finding a cat by name and displaying information
    name_to_find = 'barsik'
    found_cat = cat_db.find_cat_by_name(name_to_find)
    print(f'Found cat: {found_cat}')

    # Updating a cat's age
    new_age = 4
    cat_db.update_cat_age('barsik', new_age)
    print(f'Updated age of {name_to_find} to {new_age}.')

    # Adding a new feature to a cat
    new_feature = 'fond of fish'
    cat_db.add_cat_feature('barsik', new_feature)
    print(f'Added new feature to {name_to_find}: {new_feature}')

    # Deleting a cat by name
    name_to_delete = 'barsik'
    cat_db.delete_cat_by_name(name_to_delete)
    print(f'Deleted {name_to_delete} from the database.')

    # Finding and displaying all cats
    print('All cats in the database:')
    all_cats = cat_db.find_all_cats()
    for cat in all_cats:
        print(cat)

    # Deleting all cats
    cat_db.delete_all_cats()
    print('Deleted all cats from the database.')

    # Finding and displaying all cats
    print('All cats in the database:')
    all_cats = cat_db.find_all_cats()
    for cat in all_cats:
        print(cat)