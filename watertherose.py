from controller import Controller

start = Controller()

with start.app.app_context():
    start.app.run(debug=True, port=8080)

# To whoever's grading this:
# This actually does not work the way it was intended in this format
# The program had worked perfectly fine prior to my attempt to refractor the program
# So the following code is not what was actually ran, and was my attempt to
# refactor the code in an MVC class-relationship.
# The submitted video is running the earlier, pre-refactored code.
# Apologies in advance.