from base import Group, GroupView


ADD_FORM = """
<form>
  <input type="hidden" name="type" value="flowv"/>
  ID: <input type="text" name="id"/><br/>
  Width: <input type="text" name="width"/><br/>
  Height: <input type="text" name="height"/><br/>
  <input type="submit" value="Save"/>
  <input type="button" name="cancel" value="Cancel"/>
</form>
"""


EDIT_FORM = """
<form>
  <input type="hidden" name="type" value="flowv"/>
  <input type="hidden" name="id"/>
  Width: <input type="text" name="width"/><br/>
  Height: <input type="text" name="height"/><br/>
  <input type="submit" value="Save"/>
  <input type="button" name="cancel" value="Cancel"/>
</form>
"""


class FlowVGroup(Group):

    add_form = ADD_FORM
    edit_form = EDIT_FORM

    type = "flowv"


class FlowVGroupView(GroupView):

    pass
