#活動推薦泡泡
def event_carousel(alt_text,image_url_table,event_name_table,date_table,location_table,page_url_table,google_url_table,start_index=0):
    contents = dict()
    contents['type'] = 'carousel'
    contents['contents'] = []
    events = 0
    total_events = len(image_url_table)


    #(變數可改) 圖片、活動名稱、日期、地點、活動網址、google api 網址
    for i in range(start_index, total_events):

        #10個泡泡為一組(一次最多12個bubbles)
        if events <= 10:
            bubble =    {   "type": "carousel",
                            "contents": [
                                {
                                "type": "bubble",
                                "size": "kilo",
                                "body": {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                    {
                                        "type": "image",
                                        "url": image_url_table[i],
                                        "size": "full",
                                        "aspectMode": "cover",
                                        "aspectRatio": "2:3.5",
                                        "gravity": "top"
                                    },
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                        {
                                            "type": "box",
                                            "layout": "vertical",
                                            "contents": [
                                            {
                                                "type": "text",
                                                "text": event_name_table[i][:30] if len(event_name_table[i])<30 else event_name_table[i][:30] + '...',
                                                "size": "xl",
                                                "color": "#ffffff",
                                                "weight": "bold",
                                                "wrap": True
                                            }
                                            ],
                                            "spacing": "none"
                                        },
                                        {
                                            "type": "box",
                                            "layout": "baseline",
                                            "contents": [
                                            {
                                                "type": "text",
                                                "text": date_table[i],
                                                "color": "#ebebeb",
                                                "size": "md",
                                                "flex": 0
                                            }
                                            ],
                                            "spacing": "none",
                                            "margin": "xs"
                                        },
                                        {
                                            "type": "box",
                                            "layout": "baseline",
                                            "contents": [
                                            {
                                                "type": "text",
                                                "text": location_table[i],
                                                "color": "#ffffff",
                                                "weight": "regular"
                                            }
                                            ],
                                            "spacing": "none",
                                            "margin": "xs"
                                        },
                                        {
                                            "type": "box",
                                            "layout": "vertical",
                                            "contents": [
                                            {
                                                "type": "filler"
                                            },
                                            {
                                                "type": "box",
                                                "layout": "baseline",
                                                "contents": [
                                                {
                                                    "type": "filler"
                                                },
                                                {
                                                    "type": "icon",
                                                    "url": "https://i.imgur.com/McOT6MH.png",
                                                    "margin": "none"
                                                },
                                                {
                                                    "type": "text",
                                                    "text": "購票去",
                                                    "color": "#ffffff",
                                                    "flex": 0,
                                                    "offsetTop": "-2px",
                                                    "margin": "md"
                                                },
                                                {
                                                    "type": "filler"
                                                }
                                                ],
                                                "spacing": "sm"
                                            },
                                            {
                                                "type": "filler"
                                            }
                                            ],
                                            "borderWidth": "1px",
                                            "cornerRadius": "4px",
                                            "spacing": "md",
                                            "borderColor": "#ffffff",
                                            "margin": "xl",
                                            "height": "40px",
                                            "action": {
                                            "type": "uri",
                                            "label": "action",
                                            "uri": page_url_table[i]
                                            }
                                        },
                                        {
                                            "type": "box",
                                            "layout": "vertical",
                                            "contents": [
                                            {
                                                "type": "filler"
                                            },
                                            {
                                                "type": "box",
                                                "layout": "baseline",
                                                "contents": [
                                                {
                                                    "type": "filler"
                                                },
                                                {
                                                    "type": "icon",
                                                    "url": "https://i.imgur.com/QAg1q20.png"
                                                },
                                                {
                                                    "type": "text",
                                                    "text": "展演地點",
                                                    "color": "#ffffff",
                                                    "flex": 0,
                                                    "offsetTop": "-2px",
                                                    "margin": "sm"
                                                },
                                                {
                                                    "type": "filler"
                                                }
                                                ],
                                                "spacing": "sm"
                                            },
                                            {
                                                "type": "filler"
                                            }
                                            ],
                                            "borderWidth": "1px",
                                            "cornerRadius": "4px",
                                            "spacing": "md",
                                            "borderColor": "#ffffff",
                                            "margin": "lg",
                                            "height": "40px",
                                            "action": {
                                            "type": "uri",
                                            "label": "action",
                                            "uri": google_url_table[i]
                                            }
                                        }
                                        ],
                                        "position": "absolute",
                                        "offsetBottom": "0px",
                                        "offsetStart": "0px",
                                        "offsetEnd": "0px",
                                        "backgroundColor": "#3D3D3Dcc",
                                        "paddingAll": "20px",
                                        "paddingTop": "18px"
                                    }
                                    ],
                                    "paddingAll": "0px"
                                }
                                }
                            ]
                            }
            contents['contents'].append(bubble)
            events += 1
        #當推薦活動大於10個，第11個泡泡會顯示「推薦更多」
        else:
            bubble_end =    {
                          "type": "carousel",
                          "contents": [
                            {
                              "type": "bubble",
                              "size": "kilo",
                              "body": {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                  {
                                    "type": "image",
                                    "url": "https://images.unsplash.com/photo-1589997264694-5f6bf034c0f6?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
                                    "size": "full",
                                    "aspectMode": "cover",
                                    "aspectRatio": "2:3.5",
                                    "gravity": "top"
                                  },
                                  {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                      {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                          {
                                            "type": "filler"
                                          },
                                          {
                                            "type": "box",
                                            "layout": "baseline",
                                            "contents": [
                                              {
                                                "type": "filler"
                                              },
                                              {
                                                "type": "text",
                                                "text": "推薦更多",
                                                "color": "#ffffff",
                                                "flex": 0,
                                                "offsetTop": "-2px",
                                                "margin": "sm"
                                              },
                                              {
                                                "type": "filler"
                                              }
                                            ],
                                            "spacing": "sm"
                                          },
                                          {
                                            "type": "filler"
                                          }
                                        ],
                                        "borderWidth": "1px",
                                        "cornerRadius": "4px",
                                        "spacing": "md",
                                        "borderColor": "#ffffff",
                                        "margin": "lg",
                                        "height": "40px",
                                        "action": {
                                          "type": "postback",
                                          "data": f'show_more,{i}',
                                          "label": "推薦更多"
                                        }
                                      }
                                    ],
                                    "position": "absolute",
                                    "offsetBottom": "0px",
                                    "offsetStart": "0px",
                                    "offsetEnd": "0px",
                                    "paddingAll": "20px",
                                    "paddingTop": "18px"
                                  }
                                ],
                                "paddingAll": "0px"
                              }
                            }
                          ]
                        }
            contents['contents'].append(bubble_end)
            break

    message = FlexSendMessage(alt_text=alt_text,contents=contents)
    return message
