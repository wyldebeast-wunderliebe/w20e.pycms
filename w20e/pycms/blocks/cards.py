from base import Group, GroupView


ADD_FORM = """
<form>
  <input type="hidden" name="type" value="cards"/>
  ID: <input type="text" name="id"/><br/>
  Width: <input type="text" name="width"/><br/>
  Cols: <input type="text" name="cols"/><br/>
  <input type="submit" value="Save"/>
  <input type="button" name="cancel" value="Cancel"/>
</form>
"""


EDIT_FORM = """
<form>
  <input type="hidden" name="type" value="cards"/>
  <input type="hidden" name="id"/>
  Width: <input type="text" name="width"/><br/>
  <input type="submit" value="Save"/>
  <input type="button" name="cancel" value="Cancel"/>
</form>
"""

CARD_FORM = """
<form>
  <input type="hidden" name="type" value="card"/>
  ID: <input type="text" name="id"/><br/>
  Title: <input type="text" name="title"/><br/>
  <input type="submit" value="Save"/>
  <input type="button" name="cancel" value="Cancel"/>
</form>
"""


class CardsGroup(Group):

    add_form = ADD_FORM
    edit_form = EDIT_FORM

    type = "cards"


class CardGroup(Group):

    """ Single card """

    add_form = edit_form = CARD_FORM

    type = "card"


class CardsGroupView(GroupView):

    pass

