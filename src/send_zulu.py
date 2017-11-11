import craft
import messenger

# craft newsletter
data = craft.craft_newsletter()

# craft html
html = craft.craft_html(data)

# craft text
text = craft.craft_text(data)

# send email
messenger.send_mail(name=data["name"], subject=data["name"], preview="Everything you need to know to stay ahead.", html=html, text=text)