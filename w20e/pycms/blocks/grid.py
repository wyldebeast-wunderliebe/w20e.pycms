from base import Group, GroupView


ADD_FORM = """
<form>
  <input type="hidden" name="type" value="grid"/>
  ID: <input type="text" name="id"/><br/>
  Width: <input type="text" name="width"/><br/>
  Height: <input type="text" name="height"/><br/>
  Cols: <input type="text" name="cols"/><br/>
  Rows: <input type="text" name="rows"/><br/>
  <input type="submit" value="Save"/>
  <input type="button" name="cancel" value="Cancel"/>
</form>
"""


EDIT_FORM = """
<form>
  <input type="hidden" name="type" value="grid"/>
  <input type="hidden" name="id"/>
  Width: <input type="text" name="width"/><br/>
  Height: <input type="text" name="height"/><br/>
  <input type="submit" value="Save"/>
  <input type="button" name="cancel" value="Cancel"/>
</form>
"""


class GridGroup(Group):

    add_form = ADD_FORM
    edit_form = EDIT_FORM

    type = "grid"


class GridCellGroup(Group):

    type = "cell"


class GridRowGroup(Group):

    type = "row"


class GridGroupView(GroupView):

    pass

