from notion_client import Client
import json
import os

# Set your Notion API token
notion_token = os.environ.get('NOTION_KEY')
notion = Client(auth=notion_token)

# Function to get and print page properties
def get_page_properties(page_id):
    page = notion.pages.retrieve(page_id=page_id)
    return page['properties']

# Function to get and print block children (content)
def get_block_children(block_id):
    children = notion.blocks.children.list(block_id=block_id)
    return children['results']

# Function to find the table block ID in the page content
def find_table_block_id(block_children):
    for block in block_children:
        if block['type'] == 'table':
            return block['id']
    return None

# Function to extract table data and format it as required
def extract_table_data(block_id):
    table_data = []

    # Retrieve the children of the table block which are the rows
    table_rows = notion.blocks.children.list(block_id=block_id)['results']

    # Ignore the first row and any empty rows
    for i, row in enumerate(table_rows[1:], start=1):  # Start from the second row
        if row['type'] == 'table_row':
            cells = row['table_row']['cells']
            # Check if the row is not empty
            if cells and any(cells):
                row_data = {
                    'name': cells[0][0]['plain_text'] if cells[0] else '',
                    'price': cells[1][0]['plain_text'] if cells[1] else '',
                    'url': cells[2][0]['plain_text'] if cells[2] else ''
                }
                # Only add non-empty rows
                if row_data['name'] or row_data['price'] or row_data['url']:
                    table_data.append(row_data)

    return table_data

if __name__ == "__main__":
    # Replace with your actual page ID
    page_id = os.environ.get('NOTION_UUID')

    # Get the page properties
    page_properties = get_page_properties(page_id)
    print("Page Properties:")
    print(page_properties)

    # Get the block children (content) of the page
    block_children = get_block_children(page_id)
    print("\nPage Content:")
    for child in block_children:
        print(child)

    # Find the table block ID
    table_block_id = find_table_block_id(block_children)
    if table_block_id:

        # Extract and format the table data from the table block
        table_block_id = '1340550c-e7d4-42a8-b832-15893f0c3c60'
        formatted_data = extract_table_data(table_block_id)
        print("\nFormatted Data:")
        print(json.dumps(formatted_data, indent=4))

        # Save formatted data to a JSON file
        with open('items.json', 'w') as json_file:
            json.dump(formatted_data, json_file, indent=4)
    else:
        print("No table block found.")