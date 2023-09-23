from flask import Flask, request,jsonify
import datetime
from dotenv import load_dotenv
import os
import threading
import requests
import json
import psycopg2

load_dotenv()  
app = Flask(__name__)


@app.route('/webhook',methods = ['GET','POST'])
def webhook():
    try:
        data = request.get_json(silent=True)
        if data['queryResult']['intent']['displayName'] == '2.detail':
            detail = details(data)
            return jsonify(detail)
        
        elif data['queryResult']['intent']['displayName'] == '3.await-yes':
            result = awaitYes(data)
            return jsonify(result)
        
        elif data['queryResult']['intent']['displayName'] == '7.await-email':
            response = awaitTicket(data)
            return jsonify(response)
    except Exception as e:
        print(e)

def details(data):
    try:
        pci = data['queryResult']['parameters']['pci']    
        
        if pci.lower() == 'player' or pci.lower() == 'parent':
            reply = {
    "fulfillmentText": "How can I be of assistance today?",
    "fulfillmentMessages": [{"text": { "text": [ "How can I be of assistance today?" ]  } }, {
    "payload": {
        "richContent": [
            [
            {
                "title": "Choose from below.."
            },
            {
                "type": "chips",
                "options": [
                {
                    "text": "Registration"
                },
                {
                    "text": "Tryouts"
                },
                {
                    "text": "Uniforms"
                },
                {
                    "text": "50/50 Raffle"
                },
                {
                    "text": "Popcorn Fundraiser"
                },
                {
                    "text": "National Program"
                }
                ]
            }
            ]
        ]
        }
}
]
}

        elif pci.lower() == 'coach':
                        reply = {
                "fulfillmentText": "How can I be of assistance today?",
                "fulfillmentMessages": [{"text": { "text": [ "How can I be of assistance today?" ]  } }, {
                "payload": {
                    "richContent": [
                        [
                        {
                            "title": "Choose from below.."
                        },
                        {
                            "type": "chips",
                            "options": [
                            {
                                "text": "Registration"
                            },
                            {
                                "text": "Tryouts"
                            },
                            {
                                "text": "Tourney Budgets"
                            },
                            {
                                "text": "Coaches Pay"
                            },
                            {
                                "text": "Uniforms"
                            },
                            {
                                "text": "Team Insurance"
                            },
                            {
                                "text": "ICC / coach Resource Center / player tryout flyers / looking for coaches flyers / vector logo files / end of season player evaluation cards / etc"
                            },
                            {
                                "text": "50/50 Raffle"
                            },
                            {
                                "text": "Popcorn Fundraiser"
                            },
                            {
                                "text": "National Program"
                            }
                            ]
                        }
                        ]
                    ]
                    }
            }
            ]
            }

        else:
            reply = {
                "fulfillmentText": "How can I be of assistance today?",
                "fulfillmentMessages": [{"text": { "text": [ "How can I be of assistance today?" ]  } }, {
                "payload": {
                    "richContent": [
                        [
                        {
                            "title": "Choose from below.."
                        },
                        {
                            "type": "chips",
                            "options": [
                            {
                                "text": "Registration"
                            },
                            {
                                "text": "Tryouts"
                            },
                            {
                                "text": "Tourney Budgets"
                            },
                            {
                                "text": "Coaches Pay"
                            },
                            {
                                "text": "ICC Pay"
                            },
                            {
                                "text": "Uniforms"
                            },
                            {
                                "text": "Team Insurance"
                            },
                            {
                                "text": "ICC / coach Resource Center / player tryout flyers / looking for coaches flyers / vector logo files / end of season player evaluation cards / etc"
                            },
                            {
                                "text": "50/50 Raffle"
                            },
                            {
                                "text": "Popcorn Fundraiser"
                            },
                            {
                                "text": "National Program"
                            }
                            ]
                        }
                        ]
                    ]
                    }
            }
            ]
            }

    except Exception as e:
        print(e)
    return reply

def awaitYes(data):
    try:
        pci = data['queryResult']['parameters']['pci']
        personName = data['queryResult']['parameters']['name']['name']
        status = 'satisfied'

        DATABASE_URL = os.getenv("DATABASE_URL")
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        query1 = conn.cursor()
        query1.execute("INSERT INTO public.users ( name, pci, status) Values (%s,%s,%s)",(personName,pci,status))
        query1.close()
        conn.commit()
        reply = {
             'fulfillmentText': "Thank you. Have a great day!!!",
        }
        
    except Exception as e:
         print(e)
    return reply

def awaitTicket(data):
    try:
        personName = data['queryResult']['parameters']['name']['name']
        pci = data['queryResult']['parameters']['pci']
        email = data['queryResult']['parameters']['email']
        question = data['queryResult']['parameters']['question']
        status = 'ticket'

        DATABASE_URL = os.getenv("DATABASE_URL")
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        query1 = conn.cursor()
        query1.execute("INSERT INTO public.users ( name, pci, status) Values (%s,%s,%s)",(personName,pci,status))
        query1.close()
        conn.commit()
        ticket_thread = threading.Thread(target=createTicket, args=(personName,email,question))
        ticket_thread.start()
        reply = {
             'fulfillmentText': "Ticket has been created successfully",
        }
    except Exception as e:
        print(e)

    return reply

def createTicket(name,email,question):
    access_token = generateAccessToken()
    url = "https://desk.zoho.com/api/v1/tickets"
    payload = json.dumps({
        "subject": "Ticket Created From Chatbot",
        "departmentId": os.getenv('DepartmentID'),
        "contactId": os.getenv('ContactID'),
        "description":f"This ticket has been created by:\nName: {name}\nEmail: {email}\nQuestion: {question}"
    })
    headers = {
    'Authorization': f'Zoho-oauthtoken {access_token}',
    'orgId': os.getenv('OrgID'),
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    data = response.json()
    ticketNumber = data['ticketNumber']
    print("Ticket Created Successfully!!! Here is the ticket number: ",ticketNumber)

def generateAccessToken():
    clientID = os.getenv('ClientID')
    clientSecret = os.getenv('ClientSecret')
    refreshToken = os.getenv('RefreshToken')
    url = f"https://accounts.zoho.com/oauth/v2/token?refresh_token={refreshToken}&client_id={clientID}&client_secret={clientSecret}&grant_type=refresh_token"
    response = requests.request("POST", url)
    result = response.json()
    access_token = result['access_token']
    return access_token

if __name__ == '__main__':
    app.run(debug=True)