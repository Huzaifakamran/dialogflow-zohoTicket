from flask import Flask, request,jsonify
import datetime

app = Flask(__name__)
myList = []
@app.route('/webhook',methods = ['GET','POST'])
def webhook():
    try:
        data = request.get_json(silent=True)
        if data['queryResult']['intent']['displayName'] == '2.detail':
            detail = details(data)
            return jsonify(detail)
        
        elif data['queryResult']['intent']['displayName'] == '3.await-yes':
            result = awaitYes()
            return jsonify(result)
        
        elif data['queryResult']['intent']['displayName'] == '5.await-ticket':
            response = awaitTicket(data)
            return jsonify(response)
    except Exception as e:
        print(e)

def details(data):
    try:
        pci = data['queryResult']['parameters']['pci']
        name = data['queryResult']['parameters']['name']['name']
        mydict = {
             'name':name,
             'date':datetime.datetime.now(),
             'pci':pci
        }
        myList.append(mydict)
        
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
                                "text": "Resource center / player tryout flyer"
                            },
                            {
                                "text": "End of season player evaluation cards"
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
                                "text": "Resource center / player tryout flyer"
                            },
                            {
                                "text": "Looking for coaches flyer / vector logo files"
                            },
                            {
                                "text": "End of season player evaluation cards"
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

def awaitYes():
    try:
        mydict = {
             'status':'satisfied'
        }
        myList.append(mydict)
        print(myList)
        reply = {
             'fulfillmentText': "Thank you. Have a great day!!!",
        }
        
    except Exception as e:
         print(e)
    return reply

def awaitTicket(data):
    try:
        mydict = {
             'status':'ticket'
        }
        myList.append(mydict)
        print(myList)
        reply = {
             'fulfillmentText': "Ticket Opened",
        }
    except Exception as e:
        print(e)
    return reply

if __name__ == '__main__':
    app.run(debug=True)