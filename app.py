from api import app, routes
route = routes.AddToDb()
route.add_yesterday_data()

# if __name__ == '__main__':
#     app.run(debug=True)
