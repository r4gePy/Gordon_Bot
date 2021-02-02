KEYBOARD_START = {
    "one_time": None,
    "buttons": [
        [{
            "action": {
                "type": "text",
                "payload": "{\"button\": \"1\"}",
                "label": "Урок",
            },
            "color": "negative"
        },
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"2\"}",
                    "label": "Расписание"
                },
                "color": "positive"
            },
        ],
        [{
            "action": {
                "type": "text",
                "payload": "{\"button\": \"3\"}",
                "label": "Узнать ДЗ",
            },
            "color": "primary"
        },
        ]

    ]
}


KEYBOARD_NUMBERS_DAYS = {
    "one_time": True,
    "buttons": [
        [{
            "action": {
                "type": "text",
                "payload": "{\"button\": \"1 \"}",
                "label": "1",
            },
            "color": "secondary"
        },
            {
            "action": {
                "type": "text",
                "payload": "{\"button\": \"2 \"}",
                "label": "2",
            },
            "color": "secondary"
            },
        ],
        [{
            "action": {
                "type": "text",
                "payload": "{\"button\": \"3 \"}",
                "label": "3",
            },
            "color": "secondary"
        },
            {
            "action": {
                "type": "text",
                "payload": "{\"button\": \"4 \"}",
                "label": "4",
            },
            "color": "secondary"
            },
        ],
        [{
            "action": {
                "type": "text",
                "payload": "{\"button\": \"5 \"}",
                "label": "5",
            },
            "color": "secondary"
            },
        ]
    ]
}