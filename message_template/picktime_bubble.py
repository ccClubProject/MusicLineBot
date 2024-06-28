#選日期泡泡 
time_bubble = {
  "type": "bubble",
  "size": "kilo",
  "hero": {
    "type": "image",
    "url": "https://images.unsplash.com/photo-1496293455970-f8581aae0e3b?q=80&w=2013&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
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
        "text": "想找什麼時間呢?",
        "weight": "bold",
        "size": "lg",
        "align": "center",
        "margin": "none",
        "offsetTop": "5px"
      }
    ],
    "margin": "none",
    "spacing": "none"
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "spacing": "none",
    "contents": [
      {
        "type": "button",
        "style": "link",
        "action": {
          "type": "datetimepicker",
          "label": "選擇日期",
          "data": "action=sel_date",
          "mode": "date"
        },
        "color": "#FF4800",
        "height": "sm"
      },
      {
        "type": "button",
        "style": "link",
        "height": "sm",
        "action": {
          "type": "postback",
          "label": "不指定",
          "data": "action=no_date"
        },
        "color": "#FF4800"
      }
    ],
    "margin": "none"
  }
}
