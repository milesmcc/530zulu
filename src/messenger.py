from mailchimp3 import MailChimp

from requests.exceptions import HTTPError

import os

class MailchimpError(Exception):
    pass

client = MailChimp(os.environ['MC_USERNAME'], os.environ['MC_SECRET_KEY'])

def send_mail(name, subject, preview, html, text):
    '''
    Send an email to the entire subscriber list.
    :param name: the name of the campaign; must be unique
    :param subject: the subject of the campaign
    :param preview: the campaign preview
    :param html: the html content of the campaign
    :param text: the text-only content of the campaign
    :return: None
    '''

    # send_mail("530ZULU Hello World", "530ZULU: Hello World!", "The Preview...", "<h1>Hello World</h1>", "Hello World!")

    print("Sending to list ID: " + os.environ['MC_LIST_ID'])

    try:
        # create a campaign for the message
        campaign = client.campaigns.create(data={
            "type": "regular",
            "recipients": {
                "list_id": os.environ['MC_LIST_ID']
            },
            "settings": {
                "subject_line": subject,
                "preview_text": preview,
                "title": name,
                "from_name": "530ZULU",
                "reply_to": "530zulu@sendmiles.email",
            }
        })

        # update campaign content
        client.campaigns.content.update(campaign_id=campaign["id"], data={
            "plain_text": text,
            "html": html
        })

        # send the campaign
        client.campaigns.actions.send(campaign_id=campaign["id"])
    except HTTPError as e:
        if e.response.status_code == 400:
            json = e.response.json()
            raise MailchimpError(json.get('errors') or json.get('detail') or json)
        else:
            raise
