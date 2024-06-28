#選地點泡泡
location_bubble={
    "type": "bubble",
    "hero": {
        "type": "image",
        "url": "https://images.unsplash.com/photo-1489641493513-ba4ee84ccea9?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        "size": "full",
        "aspectRatio": "20:13",
        "aspectMode": "cover",
        "action": {
            "type": "uri",
            "uri": "https://line.me/"
        }
    },
    "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "text",
                "text": "想找哪個地區呢?",
                "weight": "bold",
                "size": "lg",
                "align": "center"
            }
        ]
    },
    "footer": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
            {
            "type": "button",
            "style": "link",
            "height": "sm",
            "action": {
                "type": "message",
                "label": "北部",
                "text": "北部"
            },
            "color": "#FF4800"
        },
        {
            "type": "button",
            "style": "link",
            "height": "sm",
            "action": {
                "type": "message",
                "label": "中部",
                "text": "中部"
        },
        "color": "#FF4800"
        },
        {
            "type": "button",
            "action": {
                "type": "message",
                "label": "南部",
                "text": "南部"
        },
        "color": "#FF4800"
        },
        {
            "type": "button",
            "action": {
                "type": "message",
                "label": "東部&離島",
                "text": "東部&離島"
        },
        "color": "#FF4800"
        },
    ],
    "flex": 0
    }
}
