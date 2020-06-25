from app import App

app = App("settings.json")
app.load_sites()
app.run()