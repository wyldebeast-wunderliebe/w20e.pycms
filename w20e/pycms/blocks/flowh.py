from base import Group, GroupView


ADD_FORM = """
<form>
  <input type="hidden" name="type" value="flowh"/>
  ID: <input type="text" name="id"/><br/>
  Width: <input type="text" name="width"/><br/>
  Height: <input type="text" name="height"/><br/>
  <input type="submit" value="Save"/>
  <input type="button" name="cancel" value="Cancel"/>
</form>
"""

EDIT_FORM = """
<form>
  <input type="hidden" name="type" value="flowh"/>
  <input type="hidden" name="id"/><br/>
  Width: <input type="text" name="width"/><br/>
  Height: <input type="text" name="height"/><br/>
  <input type="submit" value="Save"/>
  <input type="button" name="cancel" value="Cancel"/>
</form>
"""


class FlowHGroup(Group):

    add_form = ADD_FORM
    edit_form = EDIT_FORM

    type = "flowh"


class FlowHGroupView(GroupView):

    pass
