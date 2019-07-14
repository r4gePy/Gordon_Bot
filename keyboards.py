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