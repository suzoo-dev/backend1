import sqlite3
from typing import List, Optional, Union
from flask import Flask, jsonify, request
import logging
from pydantic import BaseModel


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


app = Flask(__name__)

"""
Here are two sample endpoints to test the connection to the database and posting to the server.
Here's a sample curl request to test the post to the below sample route.
curl -X POST -H "Content-Type: application/json" -d '{"test_string":"test"}' http://localhost:5001/post

Please add the endpoint to this file.

You can specify the interface to the frontend using a pydantic model like the Body model below if you want, or do something better.
"""
def sql(query, params=None):
    conn = get_db_connection()
    cur = conn.cursor()
    if params:
        cur.execute(query, params)
    else:
        cur.execute(query)
    if cur.description:
        results = cur.fetchall()
        column_names = [column[0] for column in cur.description]
        conn.close()
        return [dict(zip(column_names, row)) for row in results]
    
    conn.commit() 
    conn.close()
    return None


@app.route('/')
def sample_get_route():
    card_results = sql('SELECT * FROM card')
    deck_results = sql('SELECT * FROM deck')
    json_results = {'deck_results': deck_results, 'card_results': card_results}
    return jsonify(json_results)


"""

"""

class Body(BaseModel):
    test_string: str


@app.route('/post', methods=['POST'])
def sample_post_route():
    body = Body(**request.get_json())
    return jsonify(body.dict())


class GetDeckWithCardsRequest(BaseModel):
    deck_id: int


@app.route('/get_deck', methods=['POST'])
def get_deck():
    """A method to get all of a deck's cards and child decks
    """
    body = GetDeckWithCardsRequest(**request.get_json())
    card_results = sql(f'SELECT * FROM card WHERE deck_id = {body.deck_id}')
    deck_results = sql(f'SELECT * FROM deck WHERE parent_id = {body.deck_id}')
    json_results = {'deck_results': deck_results, 'card_results': card_results}
    return jsonify(json_results)

class Deck(BaseModel):
    deck_id: int
    name: str
    children: Optional[List[Union['Deck','Card']]]

class Card(BaseModel):
    card_id: int
    content: str

class Layout(BaseModel):
    items: List['Deck']

def update_decks_and_cards(updateList):
    # Check if deck or card
    for idx, item in enumerate(updateList):
        # Check for parent_id and set to None if not
        if not 'parent_id' in item.keys():
            item["parent_id"] = None # Default parent_id
        
        if 'children' in item.keys():
            # Update Deck data
            upsertDeck(item, idx + 1)

            # Check for children and run update on them if exist
            if item["children"] and len(item["children"]) > 0:
                for childItem in item["children"]:
                    childItem["parent_id"] = item["deck_id"] # Set parent id on each child
                update_decks_and_cards(item["children"])
        else:
            # Save parent_id as deck_id
            upsertCard(item, idx + 1)

def upsertDeck(deck, order_value):
    query = '''
        INSERT INTO deck (name, parent_id, order_value)
        VALUES (?, ?, ?)
        ON CONFLICT (name) DO UPDATE 
        SET parent_id = excluded.parent_id
            ,order_value = excluded.order_value;
    '''
    sql(query, (deck["name"], deck["parent_id"], order_value))

def upsertCard(card, order_value):
    print(card)
    query = '''
        INSERT INTO card (content, deck_id, order_value)
        VALUES (?, ?, ?)
        ON CONFLICT (content) DO UPDATE 
        SET deck_id = excluded.deck_id 
            ,order_value = excluded.order_value;
    '''
    sql(query, (card["content"], card["parent_id"], order_value))

@app.route('/update_layout', methods=['POST'])
def update_layout():
    """A method to update the relationships and ordering between decks and cards"""
    layout = Layout(**request.get_json())
    layoutDump = layout.model_dump()
    update_decks_and_cards(layoutDump["items"])

    # layout = request.get_json()
    # update_decks_and_cards(layout.items)
    return "Temporary Return"



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)