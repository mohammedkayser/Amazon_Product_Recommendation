from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)
df = pd.read_csv('Data/pre_processed.csv')

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get the product name from the dropdown menu
        product_name = request.form['product_name']

        # Retrieve product details
        product_details = retrieve_product_details(product_name)

        # Retrieve similar products
        similar_products = retrieve_similar_products(product_name)

        # Retrieve complementary products
        complementary_products = suggest_complementary_products(product_name)

        return render_template('index.html', product_list=get_product_list(), product_name=product_name, product_details=product_details, similar_products=similar_products, complementary_products=complementary_products)

    return render_template('index.html', product_list=get_product_list())

def retrieve_product_details(product_name):
    # Filter the dataset based on the input product name
    product = df[df['product_name'] == product_name]

    if product.empty:
        return "Product not found."

    # Retrieve the product details
    about_product = product['about_product'].values[0]
    review_title = product['review_title'].values[0]
    actual_price = product['actual_price'].values[0]
    discount_percentage = product['discount_percentage'].values[0]
    discounted_price = product['discounted_price'].values[0]
    img_link = product['img_link'].values[0]

    product_details = {
        'product_name': product_name,  # Add the selected product name to the dictionary
        'about_product': about_product,
        'review_title': review_title,
        'actual_price': actual_price,
        'discount_percentage': discount_percentage,
        'discounted_price': discounted_price,
        'img_link': img_link
    }

    return product_details


def retrieve_similar_products(product_name):
    # Filter the dataset based on the input product name
    product = df[df['product_name'] == product_name]

    if product.empty:
        return "Product not found."

    # Retrieve the category of the selected product
    category = product['category'].values[0]

    # Filter the dataset by matching the product's category and exclude the chosen product
    similar_products = df[(df['category'] == category) & (df['product_name'] != product_name)].sort_values(by='rating', ascending=False)

    if similar_products.empty:
        return "No similar products found."

    # Keep track of selected products
    selected_products = []

    # Retrieve the distinct similar products
    results = []
    for index, row in similar_products.iterrows():
        if row['product_name'] not in selected_products:
            results.append({
                'product_name': row['product_name'],
                'about_product': row['about_product'],
                'review_title': row['review_title'],
                'actual_price': row['actual_price'],
                'discount_percentage': row['discount_percentage'],
                'discounted_price': row['discounted_price'],
                'img_link': row['img_link']
            })
            selected_products.append(row['product_name'])

        # Break the loop after finding 5 distinct similar products
        if len(selected_products) == 5:
            break

    return results

def suggest_complementary_products(product_name):
    # Filter the dataset based on the input product name
    product = df[df['product_name'] == product_name]

    if product.empty:
        return "Product not found."

    # Retrieve the category of the selected product
    category = product['category'].values[0]

    # Filter the dataset by matching the product's category and exclude the chosen product
    filtered_products = df[(df['category'] == category) & (df['product_name'] != product_name)]

    if filtered_products.empty:
        return "No complementary products found."

    # Keep track of selected products
    selected_products = []

    # Sort the filtered dataset based on discounted price (in descending order)
    suggested_products = filtered_products.sort_values(by='discounted_price', ascending=False)

    # Retrieve the suggested complementary products
    results = []
    for index, row in suggested_products.iterrows():
        if row['product_name'] not in selected_products:
            results.append({
                'product_name': row['product_name'],
                'about_product': row['about_product'],
                'review_title': row['review_title'],
                'actual_price': row['actual_price'],
                'discount_percentage': row['discount_percentage'],
                'discounted_price': row['discounted_price'],
                'img_link': row['img_link']
            })
            selected_products.append(row['product_name'])

        # Break the loop after finding 5 distinct products
        if len(selected_products) == 5:
            break

    if not results:
        return "No complementary products found."

    return results

def get_product_list():
    # Get the list of available product names
    product_list = df['product_name'].unique().tolist()

    return product_list

if __name__ == '__main__':
    app.run(debug=True)


